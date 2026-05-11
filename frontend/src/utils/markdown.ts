/** Lightweight markdown parser → structured blocks for uni-app native rendering */

export type InlineToken =
  | { type: 'text'; content: string }
  | { type: 'bold'; content: string }
  | { type: 'italic'; content: string }
  | { type: 'code'; content: string }
  | { type: 'link'; content: string; href: string }

export type Block =
  | { type: 'heading'; level: number; tokens: InlineToken[] }
  | { type: 'paragraph'; tokens: InlineToken[] }
  | { type: 'list'; ordered: boolean; items: InlineToken[][] }
  | { type: 'blockquote'; content: string }
  | { type: 'codeblock'; lang: string; content: string }
  | { type: 'hr' }

// --- Inline parsing ---

function parseInline(text: string): InlineToken[] {
  const tokens: InlineToken[] = []
  // Match bold **text**, italic *text*, inline `code`, links [text](url)
  const re = /(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`|\[(.+?)\]\((.+?)\))/g
  let lastIndex = 0
  let m: RegExpExecArray | null

  while ((m = re.exec(text)) !== null) {
    if (m.index > lastIndex) {
      tokens.push({ type: 'text', content: text.slice(lastIndex, m.index) })
    }
    if (m[2]) tokens.push({ type: 'bold', content: m[2] })
    else if (m[3]) tokens.push({ type: 'italic', content: m[3] })
    else if (m[4]) tokens.push({ type: 'code', content: m[4] })
    else if (m[5] && m[6]) tokens.push({ type: 'link', content: m[5], href: m[6] })
    lastIndex = m.index + m[0].length
  }

  if (lastIndex < text.length) {
    tokens.push({ type: 'text', content: text.slice(lastIndex) })
  }
  return tokens.length ? tokens : [{ type: 'text', content: text }]
}

// --- Block parsing ---

export function parseMarkdown(text: string): Block[] {
  if (!text) return []
  const lines = text.split('\n')
  const blocks: Block[] = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    // Empty line
    if (!line.trim()) { i++; continue }

    // Code block
    if (line.trim().startsWith('```')) {
      const lang = line.trim().slice(3).trim()
      const codeLines: string[] = []
      i++
      while (i < lines.length && !lines[i].trim().startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      i++ // skip closing ```
      blocks.push({ type: 'codeblock', lang, content: codeLines.join('\n') })
      continue
    }

    // Heading
    const headingMatch = line.match(/^(#{1,3})\s+(.+)/)
    if (headingMatch) {
      blocks.push({ type: 'heading', level: headingMatch[1].length, tokens: parseInline(headingMatch[2].trim()) })
      i++
      continue
    }

    // Horizontal rule
    if (/^(-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      blocks.push({ type: 'hr' })
      i++
      continue
    }

    // Blockquote
    if (line.startsWith('>')) {
      const quoteLines: string[] = []
      while (i < lines.length && lines[i].startsWith('>')) {
        quoteLines.push(lines[i].replace(/^>\s?/, ''))
        i++
      }
      blocks.push({ type: 'blockquote', content: quoteLines.join('\n') })
      continue
    }

    // Unordered list
    if (/^(\s*)[-*]\s+/.test(line)) {
      const items: InlineToken[][] = []
      while (i < lines.length && /^(\s*)[-*]\s+/.test(lines[i])) {
        items.push(parseInline(lines[i].replace(/^(\s*)[-*]\s+/, '')))
        i++
      }
      blocks.push({ type: 'list', ordered: false, items })
      continue
    }

    // Ordered list
    if (/^\s*\d+\.\s+/.test(line)) {
      const items: InlineToken[][] = []
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        items.push(parseInline(lines[i].replace(/^\s*\d+\.\s+/, '')))
        i++
      }
      blocks.push({ type: 'list', ordered: true, items })
      continue
    }

    // Paragraph (default)
    const paraLines: string[] = []
    while (i < lines.length && lines[i].trim() && !lines[i].startsWith('#') && !lines[i].startsWith('```') && !lines[i].startsWith('>') && !/^(\s*)[-*]\s+/.test(lines[i]) && !/^\s*\d+\.\s+/.test(lines[i])) {
      paraLines.push(lines[i])
      i++
    }
    if (paraLines.length) {
      blocks.push({ type: 'paragraph', tokens: parseInline(paraLines.join('\n')) })
    }
  }

  return blocks
}
