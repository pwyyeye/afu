import uuid
import base64
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.medical_report import MedicalReport
from app.models.report_indicator import ReportIndicator
from app.schemas.report import (
    ReportUploadResponse, ReportResponse, IndicatorResponse, TrendData,
)
from app.services.report_service import analyze_report
from app.services.llm_service import llm_service
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.post("/upload", response_model=ReportUploadResponse)
async def upload_report(
    file: UploadFile = File(...),
    family_member_id: Optional[str] = Form(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    content = await file.read()
    image_base64 = base64.b64encode(content).decode("utf-8")

    # Use Qwen-VL to extract text from image
    ocr_prompt = "请仔细阅读这张体检报告图片，提取所有可见的文字内容，包括检查项目名称、数值、参考范围等。请完整输出所有文字。"
    raw_text = llm_service.analyze_image(image_base64, ocr_prompt)

    # Analyze the extracted text
    report = analyze_report(
        db=db,
        user_id=str(user.id),
        raw_text=raw_text,
        title=file.filename or "体检报告",
        family_member_id=family_member_id,
    )

    return ReportUploadResponse(
        report_id=str(report.id),
        status=report.status,
    )


@router.get("", response_model=List[dict])
def list_reports(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reports = (
        db.query(MedicalReport)
        .filter(MedicalReport.user_id == str(user.id))
        .order_by(MedicalReport.created_at.desc())
        .all()
    )
    return [
        {
            "id": str(r.id),
            "title": r.title,
            "hospital": r.hospital,
            "report_date": str(r.report_date) if r.report_date else None,
            "overall_light": r.overall_light,
            "status": r.status,
            "created_at": r.created_at.isoformat(),
        }
        for r in reports
    ]


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    report = (
        db.query(MedicalReport)
        .filter(MedicalReport.id == report_id, MedicalReport.user_id == str(user.id))
        .first()
    )
    if not report:
        raise NotFoundException("报告不存在")

    indicators = (
        db.query(ReportIndicator)
        .filter(ReportIndicator.report_id == report_id)
        .order_by(ReportIndicator.sort_order)
        .all()
    )

    return ReportResponse(
        id=str(report.id),
        title=report.title,
        hospital=report.hospital,
        report_date=report.report_date,
        overall_light=report.overall_light,
        summary=report.summary,
        indicators=[
            IndicatorResponse(
                id=str(i.id),
                name=i.name,
                name_en=i.name_en,
                value=i.value,
                unit=i.unit,
                reference_range=i.reference_range,
                light=i.light,
                explanation=i.explanation,
                trend=i.trend,
            )
            for i in indicators
        ],
        action_plan=report.action_plan,
        status=report.status,
        created_at=report.created_at,
    )


@router.get("/compare", response_model=List[TrendData])
def compare_reports(
    indicator_names: str = "",
    years: str = "",
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not indicator_names:
        return []

    names = [n.strip() for n in indicator_names.split(",")]
    year_list = [y.strip() for y in years.split(",") if y.strip()]

    reports = (
        db.query(MedicalReport)
        .filter(
            MedicalReport.user_id == str(user.id),
            MedicalReport.status == "completed",
        )
        .order_by(MedicalReport.report_date)
        .all()
    )

    if year_list:
        reports = [r for r in reports if r.report_date and str(r.report_date.year) in year_list]

    result = []
    for name in names:
        trend_points = []
        for report in reports:
            indicator = (
                db.query(ReportIndicator)
                .filter(
                    ReportIndicator.report_id == str(report.id),
                    ReportIndicator.name == name,
                )
                .first()
            )
            if indicator and indicator.value:
                try:
                    value = float(indicator.value)
                    year = str(report.report_date.year) if report.report_date else "未知"
                    trend_points.append({"year": year, "value": value})
                except ValueError:
                    pass

        if trend_points:
            unit = None
            for report in reports:
                ind = (
                    db.query(ReportIndicator)
                    .filter(
                        ReportIndicator.report_id == str(report.id),
                        ReportIndicator.name == name,
                    )
                    .first()
                )
                if ind and ind.unit:
                    unit = ind.unit
                    break
            result.append(TrendData(name=name, unit=unit, data=trend_points))

    return result
