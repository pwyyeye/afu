import json
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.medical_report import MedicalReport
from app.models.report_indicator import ReportIndicator
from app.services.llm_service import llm_service


def load_prompt(filename: str) -> str:
    try:
        with open(f"prompts/{filename}", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


REPORT_ANALYSIS_PROMPT = """你是一位专业的医学报告分析师。请分析以下体检报告内容，提取所有检查指标。

对每个指标，请判断其健康状态：
- 红色(red): 需要立即就医或紧急处理
- 黄色(yellow): 需要关注，建议复查
- 蓝色(blue): 处于临界值，建议随访
- 绿色(green): 正常范围

请用JSON格式返回：
{
  "indicators": [
    {
      "name": "指标名称",
      "name_en": "英文缩写",
      "value": "检测值",
      "unit": "单位",
      "reference_range": "参考范围",
      "light": "red/yellow/blue/green",
      "explanation": "通俗易懂的解释"
    }
  ],
  "overall_light": "red/yellow/blue/green",
  "summary": "整体健康状况总结",
  "action_plan": [
    {
      "title": "建议标题",
      "description": "详细描述",
      "priority": "red/yellow/blue/green",
      "category": "checkup/diet/exercise/medication/lifestyle"
    }
  ]
}"""


def analyze_report(db: Session, user_id: str, raw_text: str, title: str = "体检报告",
                   hospital: str = None, report_date=None, family_member_id: str = None) -> MedicalReport:
    report = MedicalReport(
        id=str(uuid.uuid4()),
        user_id=user_id,
        family_member_id=family_member_id,
        title=title,
        hospital=hospital,
        report_date=report_date,
        raw_text=raw_text,
        status="processing",
    )
    db.add(report)
    db.flush()

    try:
        messages = [
            {"role": "system", "content": REPORT_ANALYSIS_PROMPT},
            {"role": "user", "content": f"请分析以下体检报告：\n\n{raw_text}"},
        ]
        result = llm_service.chat_json(messages, temperature=0.3)
        data = json.loads(result)

        report.overall_light = data.get("overall_light", "green")
        report.summary = data.get("summary", "")
        report.action_plan = data.get("action_plan", [])
        report.status = "completed"

        for idx, ind in enumerate(data.get("indicators", [])):
            indicator = ReportIndicator(
                id=str(uuid.uuid4()),
                report_id=report.id,
                name=ind.get("name", ""),
                name_en=ind.get("name_en"),
                value=ind.get("value"),
                unit=ind.get("unit"),
                reference_range=ind.get("reference_range"),
                light=ind.get("light", "green"),
                explanation=ind.get("explanation"),
                sort_order=idx,
            )
            db.add(indicator)

        db.commit()
    except Exception as e:
        report.status = "failed"
        report.summary = f"分析失败: {str(e)}"
        db.commit()

    return report
