"""
Trắc nghiệm tiếng khỉ — tiếng người
Flask app: chọn từ bên phải (tiếng người) tương ứng với từ bên trái (tiếng khỉ).
Chạy:   pip install flask
        python app.py
        Mở http://127.0.0.1:5000
"""
from flask import Flask, render_template_string, request, jsonify, session
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# (tiếng khỉ, [các đáp án tiếng người chấp nhận])
VOCAB = [
    ("Bang", ["Tiểu bang"]),
    ("Báo cáo", ["Thưa trình", "Nói", "Kể"]),
    ("Bảo quản", ["Che chở", "Giữ gìn", "Bảo vệ"]),
    ("Bài nói", ["Diễn văn"]),
    ("Bảo hiểm (mũ)", ["An toàn (mũ)"]),
    ("Bèo", ["Rẻ tiền"]),
    ("Bồi dưỡng", ["Nghỉ ngơi", "Tẩm bổ", "Săn sóc", "Chăm nom"]),
    ("Bóng đá", ["Đá banh", "Túc cầu"]),
    ("Bức xúc", ["Dồn nén", "Bực tức"]),
    ("Bất ngờ", ["Ngạc nhiên"]),
    ("Bổ sung", ["Thêm", "Bổ túc"]),
    ("Cách ly", ["Cô lập"]),
    ("Cảnh báo", ["Báo động", "Phải chú ý"]),
    ("Cái A-lô", ["Cái điện thoại"]),
    ("Cái đài", ["Radio", "Máy phát thanh"]),
    ("Căn hộ", ["Căn nhà"]),
    ("Căng (lắm)", ["Căng thẳng"]),
    ("Cầu lông", ["Vũ cầu"]),
    ("Chảnh", ["Kiêu ngạo", "Làm tàng"]),
    ("Chất lượng", ["Phẩm chất tốt"]),
    ("Chất xám", ["Trí tuệ", "Sự thông minh"]),
    ("Chế độ", ["Quy chế"]),
    ("Chỉ đạo", ["Chỉ thị", "Ra lệnh"]),
    ("Chỉ tiêu", ["Định suất"]),
    ("Chủ nhiệm", ["Trưởng ban", "Khoa trưởng"]),
    ("Chủ trì", ["Chủ tọa"]),
    ("Chữa cháy", ["Cứu hỏa"]),
    ("Chiêu đãi", ["Thết đãi"]),
    ("Chui", ["Lén lút"]),
    ("Chuyên chở", ["Nói lên", "Nêu ra"]),
    ("Chuyển ngữ", ["Dịch"]),
    ("Chứng minh nhân dân", ["Thẻ Căn cước"]),
    ("Chủ đạo", ["Chính"]),
    ("Co cụm", ["Thu hẹp"]),
    ("Công đoàn", ["Nghiệp đoàn"]),
    ("Công nghiệp", ["Kỹ nghệ"]),
    ("Công trình", ["Công tác"]),
    ("Cơ bản", ["Căn bản"]),
    ("Cơ khí", ["Cầu kỳ", "Phức tạp"]),
    ("Cơ sở", ["Căn bản", "Nguồn gốc"]),
    ("Cửa khẩu", ["Phi cảng", "Hải cảng"]),
    ("Cụm từ", ["Nhóm chữ"]),
    ("Cứu hộ", ["Cứu cấp"]),
    ("Diện", ["Thành phần"]),
    ("Dự kiến", ["Phỏng định"]),
    ("Đào tị", ["Tị nạn"]),
    ("Đầu ra", ["Xuất lượng"]),
    ("Đầu vào", ["Nhập lượng"]),
    ("Đại táo", ["Nấu ăn chung", "Ăn tập thể"]),
    ("Tiểu táo", ["Nấu ăn riêng", "Ăn gia đình"]),
    ("Đại trà", ["Quy mô", "Cỡ lớn"]),
    ("Đảm bảo", ["Bảo đảm"]),
    ("Đăng ký", ["Ghi danh", "Ghi tên"]),
    ("Đáp án", ["Kết quả", "Trả lời"]),
    ("Đề xuất", ["Đề nghị"]),
    ("Đội ngũ", ["Hàng ngũ"]),
    ("Động não", ["Vận dụng trí óc", "Suy luận", "Suy nghĩ"]),
    ("Đồng bào dân tộc", ["Đồng bào sắc tộc"]),
    ("Động thái", ["Động lực"]),
    ("Động viên", ["Khuyến khích"]),
    ("Đột xuất", ["Bất ngờ"]),
    ("Đường băng", ["Phi đạo"]),
    ("Đường cao tốc", ["Xa lộ"]),
    ("Gia công", ["Làm ăn công"]),
    ("Giải phóng", ["Lấy lại", "Đem đi"]),
    ("Giải phóng mặt bằng", ["Ủi cho đất bằng"]),
    ("Giản đơn", ["Đơn giản"]),
    ("Giao lưu", ["Giao thiệp", "Trao đổi"]),
    ("Hạch toán", ["Kế toán"]),
    ("Hải quan", ["Quan Thuế"]),
    ("Hàng không dân dụng", ["Hàng không dân sự"]),
    ("Hát đôi", ["Song ca"]),
    ("Hát tốp", ["Hợp ca"]),
    ("Hạt nhân", ["Nguyên tử"]),
    ("Hậu cần", ["Tiếp liệu"]),
    ("Học vị", ["Bằng cấp"]),
    ("Hệ quả", ["Hậu quả"]),
    ("Hiện đại", ["Tối tân"]),
    ("Hộ Nhà", ["Gia đình"]),
    ("Hộ chiếu", ["Sổ Thông hành"]),
    ("Hồ hởi", ["Phấn khởi"]),
    ("Hộ khẩu", ["Tờ khai gia đình"]),
    ("Hội chữ thập đỏ", ["Hội Hồng Thập Tự"]),
    ("Hoành tráng", ["Nguy nga", "Tráng lệ", "Đồ sộ"]),
    ("Hưng phấn", ["Kích động", "Vui sướng"]),
    ("Hữu hảo", ["Tốt đẹp"]),
    ("Hữu nghị", ["Thân hữu"]),
    ("Huyện", ["Quận"]),
    ("Kênh", ["Băng tần"]),
    ("Khẩn trương", ["Nhanh lên"]),
    ("Khâu", ["Bộ phận", "Nhóm", "Ngành", "Ban", "Khoa"]),
    ("Kiều hối", ["Ngoại tệ"]),
    ("Kiệt suất", ["Giỏi", "Xuất sắc"]),
    ("Kinh qua", ["Trải qua"]),
    ("Làm gái", ["Làm điếm"]),
    ("Làm việc", ["Thẩm vấn", "Điều tra"]),
    ("Lầu năm góc", ["Ngũ Giác Đài"]),
    ("Nhà trắng", ["Tòa Bạch Ốc"]),
    ("Liên hoan", ["Đại hội", "Ăn mừng"]),
    ("Liên hệ", ["Liên lạc"]),
    ("Linh tinh", ["Vớ vẩn"]),
    ("Lính gái", ["Nữ quân nhân"]),
    ("Lính thủy đánh bộ", ["Thủy quân lục chiến"]),
    ("Lợi nhuận", ["Lợi tức"]),
    ("Lược tóm", ["Tóm lược"]),
    ("Lý giải", ["Giải thích"]),
    ("Máy bay lên thẳng", ["Trực thăng"]),
    ("Múa đôi", ["Khiêu vũ"]),
    ("Nắm bắt", ["Nắm vững"]),
    ("Năng nổ", ["Siêng năng", "Tháo vát"]),
    ("Nghệ nhân", ["Thợ", "Nghệ sĩ"]),
    ("Nghệ danh", ["Tên nghệ sĩ"]),
    ("Nghĩa vụ quân sự", ["Đi quân dịch"]),
    ("Nghiêm túc", ["Nghiêm chỉnh"]),
    ("Nghiệp dư", ["Nghề phụ", "Nghề tay trái"]),
    ("Nhà khách", ["Khách sạn"]),
    ("Nhất trí", ["Đồng lòng", "Đồng ý"]),
    ("Nhất quán", ["Luôn luôn", "Trước sau như một"]),
    ("Người nước ngoài", ["Ngoại kiều"]),
    ("Nỗi niềm", ["Vẻ suy tư"]),
    ("Phần cứng", ["Cương liệu"]),
    ("Phần mềm", ["Nhu liệu"]),
    ("Phản ánh", ["Phản ảnh"]),
    ("Phản hồi", ["Trả lời", "Hồi âm"]),
    ("Phát sóng", ["Phát thanh"]),
    ("Phó Tiến Sĩ", ["Cao Học"]),
    ("Phi khẩu", ["Phi trường", "Phi cảng"]),
    ("Phi vụ", ["Thương vụ"]),
    ("Phục hồi nhân phẩm", ["Hoàn lương"]),
    ("Phương án", ["Kế hoạch"]),
    ("Quá tải", ["Quá sức", "Quá mức"]),
    ("Quán triệt", ["Hiểu rõ"]),
    ("Quản lý", ["Quản trị"]),
    ("Quảng trường", ["Công trường"]),
    ("Quân hàm", ["Cấp bực"]),
    ("Quy hoạch", ["Kế hoạch"]),
    ("Quy trình", ["Tiến trình"]),
    ("Sốc", ["Kinh hoàng", "Kinh ngạc", "Ngạc nhiên"]),
    ("Sơ tán", ["Tản cư"]),
    ("Sư", ["Sư đoàn"]),
    ("Sức khỏe công dân", ["Y tế công cộng"]),
    ("Sự cố", ["Trở ngại"]),
    ("Tập đoàn", ["Công ty"]),
    ("Doanh nghiệp", ["Công ty"]),
    ("Tên lửa", ["Hỏa tiễn"]),
    ("Tham gia lưu thông", ["Lưu hành"]),
    ("Tham quan", ["Thăm viếng"]),
    ("Thanh lý", ["Thanh toán", "Chứng minh"]),
    ("Thân thương", ["Thân mến"]),
    ("Thi công", ["Làm"]),
    ("Thị phần", ["Thị trường"]),
    ("Thu nhập", ["Lợi tức"]),
    ("Thư giãn", ["Tỉnh táo", "Giải trí"]),
    ("Thuyết phục", ["Có lý", "Hợp lý", "Tin được"]),
    ("Tiên tiến", ["Xuất sắc"]),
    ("Tiến công", ["Tấn công"]),
    ("Tiếp thu", ["Tiếp nhận", "Thâu nhận", "Lãnh hội"]),
    ("Tiêu dùng", ["Tiêu thụ"]),
    ("Tổ lái", ["Phi hành đoàn"]),
    ("Tờ rơi", ["Truyền đơn"]),
    ("Tranh thủ", ["Cố gắng"]),
    ("Trí tuệ", ["Kiến thức"]),
    ("Triển khai", ["Khai triển"]),
    ("Tư duy", ["Suy nghĩ"]),
    ("Tư liệu", ["Tài liệu"]),
    ("Từ", ["Tiếng", "Chữ"]),
    ("Ùn tắc", ["Tắc nghẽn"]),
    ("Vấn nạn", ["Vấn đề"]),
    ("Vận động viên", ["Lực sĩ"]),
    ("Viện Ung Bướu", ["Viện Ung Thư"]),
    ("Vô tư", ["Tự nhiên"]),
    ("Xác tín", ["Chính xác"]),
    ("Xe con", ["Xe du lịch"]),
    ("Xe khách", ["Xe đò"]),
    ("Xử lý", ["Giải quyết", "Thi hành"]),
]


def pick_distractors(correct_pair, valid_answers, n=3):
    """Lấy n đáp án sai, đảm bảo không trùng với đáp án đúng."""
    pool = [v for v in VOCAB if v[0] != correct_pair[0]]
    random.shuffle(pool)
    distractors = []
    for p in pool:
        cand = random.choice(p[1])
        if cand in valid_answers or cand in distractors:
            continue
        distractors.append(cand)
        if len(distractors) >= n:
            break
    return distractors


@app.route("/")
def index():
    session.setdefault("score", 0)
    session.setdefault("total", 0)
    session.setdefault("seen", [])
    return render_template_string(PAGE)


@app.route("/question")
def question():
    seen = session.get("seen", [])
    available = [v for v in VOCAB if v[0] not in seen]
    if not available:
        seen = []
        available = VOCAB
        session["seen"] = seen

    pair = random.choice(available)
    seen.append(pair[0])
    session["seen"] = seen

    khi, valid = pair
    correct = random.choice(valid)
    distractors = pick_distractors(pair, valid)
    options = [correct] + distractors
    random.shuffle(options)

    session["current_valid"] = valid

    return jsonify({
        "question": khi,
        "options": options,
        "remaining": len(VOCAB) - len(seen),
        "total_vocab": len(VOCAB),
    })


@app.route("/answer", methods=["POST"])
def answer():
    selected = (request.get_json() or {}).get("answer", "")
    valid = session.get("current_valid", [])
    is_correct = selected in valid

    session["total"] = session.get("total", 0) + 1
    if is_correct:
        session["score"] = session.get("score", 0) + 1

    return jsonify({
        "correct": is_correct,
        "valid_answers": valid,
        "score": session["score"],
        "total": session["total"],
    })


@app.route("/reset", methods=["POST"])
def reset():
    session["score"] = 0
    session["total"] = 0
    session["seen"] = []
    return jsonify({"ok": True})


PAGE = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tiếng khỉ — Tiếng người</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#f4ecd8;
    --paper-deep:#ebe0c4;
    --ink:#1f1a14;
    --ink-soft:#5a4d3a;
    --rule:#cbbf9f;
    --accent:#8b2e2e;       /* mực đỏ son */
    --accent-soft:#c2786e;
    --green:#3d6b3a;
    --green-soft:#aac49a;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{height:100%}
  body{
    font-family:"EB Garamond", Georgia, serif;
    color:var(--ink);
    background:
      radial-gradient(ellipse at 20% 10%, rgba(255,255,255,.5), transparent 50%),
      radial-gradient(ellipse at 80% 90%, rgba(139,46,46,.06), transparent 60%),
      var(--paper);
    background-attachment: fixed;
    min-height:100vh;
    display:flex; align-items:flex-start; justify-content:center;
    padding:48px 20px 60px;
    position:relative;
  }
  /* hạt giấy */
  body::before{
    content:"";
    position:fixed; inset:0; pointer-events:none; z-index:0;
    background-image:
      radial-gradient(rgba(31,26,20,.06) 1px, transparent 1px),
      radial-gradient(rgba(31,26,20,.04) 1px, transparent 1px);
    background-size: 3px 3px, 7px 7px;
    background-position: 0 0, 1px 2px;
    mix-blend-mode: multiply;
    opacity:.6;
  }
  .sheet{
    position:relative; z-index:1;
    width:100%; max-width:680px;
    background:linear-gradient(180deg,#f7f0dc 0%, #f1e7cb 100%);
    border:1px solid var(--rule);
    box-shadow:
      0 1px 0 #fff inset,
      0 30px 60px -30px rgba(40,28,10,.35),
      0 12px 24px -12px rgba(40,28,10,.25);
    padding: 44px 48px 36px;
    border-radius: 2px;
  }
  .sheet::before{
    content:""; position:absolute; left:0; right:0; top:0; height:8px;
    background:repeating-linear-gradient(90deg, var(--accent) 0 14px, transparent 14px 28px);
    opacity:.85;
  }
  .masthead{
    display:flex; align-items:flex-end; justify-content:space-between;
    border-bottom:1px solid var(--rule);
    padding-bottom:18px; margin-bottom:28px;
  }
  .masthead .title{
    font-family:"Cormorant Garamond", serif;
    font-weight:700;
    font-size: clamp(28px, 4.4vw, 38px);
    letter-spacing:-.01em;
    line-height:1;
  }
  .masthead .title em{
    font-style: italic; color: var(--accent); font-weight:600;
  }
  .masthead .meta{
    font-family:"JetBrains Mono", monospace;
    font-size:11px; letter-spacing:.14em; text-transform:uppercase;
    color:var(--ink-soft); text-align:right; line-height:1.6;
  }
  .scorebar{
    display:flex; justify-content:space-between; align-items:center;
    font-family:"JetBrains Mono", monospace; font-size:12px;
    color:var(--ink-soft); letter-spacing:.08em;
    padding:10px 0 22px;
    border-bottom:1px dashed var(--rule); margin-bottom:24px;
  }
  .scorebar b{ color:var(--ink); font-weight:500; }
  .scorebar .right{ text-align:right; }

  .prompt-label{
    font-family:"JetBrains Mono", monospace;
    font-size:11px; letter-spacing:.22em; text-transform:uppercase;
    color:var(--accent); margin-bottom:8px; text-align:center;
  }
  .question{
    text-align:center;
    font-family:"Cormorant Garamond", serif;
    font-style: italic;
    font-weight:500;
    font-size: clamp(40px, 7vw, 64px);
    line-height:1.05;
    padding: 18px 12px 26px;
    color: var(--ink);
    position:relative;
  }
  .question::before, .question::after{
    content:"❧";
    color: var(--accent-soft);
    font-style:normal;
    display:block;
    font-size:14px;
    letter-spacing:.5em;
    margin:4px 0;
  }
  .options{
    display:grid; gap:10px;
    margin-top:6px;
  }
  .opt{
    appearance:none;
    cursor:pointer;
    text-align:left;
    font-family:"EB Garamond", serif;
    font-size:19px;
    color:var(--ink);
    background:transparent;
    border:1px solid var(--rule);
    border-left:3px solid var(--rule);
    padding:14px 18px;
    border-radius:1px;
    transition: background .15s, border-color .15s, transform .08s;
    display:flex; align-items:baseline; gap:14px;
  }
  .opt .letter{
    font-family:"JetBrains Mono", monospace;
    font-size:11px; letter-spacing:.1em;
    color:var(--ink-soft);
    min-width:18px;
  }
  .opt:hover:not(:disabled){
    background:rgba(139,46,46,.05);
    border-left-color:var(--accent);
  }
  .opt:active:not(:disabled){ transform: translateY(1px); }
  .opt:disabled{ cursor:default; }
  .opt.correct{
    background:rgba(61,107,58,.12);
    border-color:var(--green);
    border-left-color:var(--green);
    color:var(--green);
  }
  .opt.correct .letter{ color:var(--green); }
  .opt.wrong{
    background:rgba(139,46,46,.10);
    border-color:var(--accent);
    border-left-color:var(--accent);
    color:var(--accent);
    text-decoration: line-through;
    text-decoration-color: var(--accent-soft);
  }
  .opt.wrong .letter{ color:var(--accent); }

  .feedback{
    margin-top:20px;
    min-height:24px;
    font-style:italic;
    font-size:16px;
    text-align:center;
    color: var(--ink-soft);
  }
  .feedback.correct{ color: var(--green); }
  .feedback.wrong  { color: var(--accent); }
  .feedback .alt{
    display:block;
    font-size:13px;
    margin-top:4px;
    color:var(--ink-soft);
    font-style:normal;
    font-family:"JetBrains Mono", monospace;
    letter-spacing:.04em;
  }

  .actions{
    display:flex; justify-content:space-between; align-items:center;
    margin-top:24px; padding-top:18px;
    border-top:1px solid var(--rule);
  }
  .next{
    appearance:none; cursor:pointer;
    font-family:"Cormorant Garamond", serif;
    font-weight:600;
    font-size:17px;
    letter-spacing:.02em;
    background:var(--ink); color:var(--paper);
    border:none;
    padding:12px 22px;
    border-radius:1px;
    transition: opacity .15s, transform .08s;
  }
  .next:hover:not(:disabled){ opacity:.88; }
  .next:active:not(:disabled){ transform: translateY(1px); }
  .next:disabled{ opacity:.35; cursor:not-allowed; }
  .reset{
    appearance:none; cursor:pointer; background:none; border:none;
    color:var(--ink-soft); font-family:"JetBrains Mono", monospace;
    font-size:11px; letter-spacing:.18em; text-transform:uppercase;
    text-decoration: underline; text-underline-offset: 4px;
  }
  .reset:hover{ color:var(--accent); }

  .footnote{
    text-align:center; margin-top:18px;
    font-family:"JetBrains Mono", monospace;
    font-size:10px; letter-spacing:.18em; text-transform:uppercase;
    color:var(--ink-soft); opacity:.7;
  }
  @media (max-width:520px){
    .sheet{ padding:30px 22px 26px; }
    .masthead{ flex-direction:column; align-items:flex-start; gap:10px;}
    .masthead .meta{ text-align:left; }
  }
</style>
</head>
<body>
  <main class="sheet">
    <header class="masthead">
      <div class="title">Tiếng <em>khỉ</em> &mdash; Tiếng <em>người</em></div>
      <div class="meta">
        Trắc&nbsp;nghiệm từ&nbsp;vựng<br>
        Ấn&nbsp;bản dành cho Agness
      </div>
    </header>

    <div class="scorebar">
      <span>Điểm — <b id="score">0</b> / <b id="total">0</b></span>
      <span class="right">Còn lại — <b id="remaining">—</b> / <b id="totalvocab">—</b></span>
    </div>

    <div class="prompt-label">Tiếng khỉ</div>
    <div class="question" id="question">…</div>

    <div class="options" id="options"></div>

    <div class="feedback" id="feedback"></div>

    <div class="actions">
      <button class="reset" id="resetBtn" type="button">Làm lại</button>
      <button class="next" id="nextBtn" type="button" disabled>Câu tiếp →</button>
    </div>

    <div class="footnote">— hết trang —</div>
  </main>

<script>
const $ = id => document.getElementById(id);
let answered = false;

async function loadQuestion(){
  answered = false;
  $('feedback').textContent = '';
  $('feedback').className = 'feedback';
  $('nextBtn').disabled = true;
  $('options').innerHTML = '';
  $('question').textContent = '…';

  const r = await fetch('/question');
  const d = await r.json();

  $('question').textContent = d.question;
  $('remaining').textContent = d.remaining;
  $('totalvocab').textContent = d.total_vocab;

  const letters = ['A','B','C','D','E','F'];
  d.options.forEach((opt, i) => {
    const b = document.createElement('button');
    b.className = 'opt';
    b.type = 'button';
    b.innerHTML = `<span class="letter">${letters[i]}</span><span>${opt}</span>`;
    b.addEventListener('click', () => submit(opt, b));
    $('options').appendChild(b);
  });
}

async function submit(answer, btn){
  if (answered) return;
  answered = true;

  const r = await fetch('/answer', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({answer})
  });
  const d = await r.json();

  document.querySelectorAll('.opt').forEach(b => {
    b.disabled = true;
    const label = b.querySelector('span:last-child').textContent;
    if (d.valid_answers.includes(label)) b.classList.add('correct');
    else if (b === btn) b.classList.add('wrong');
  });

  const fb = $('feedback');
  if (d.correct){
    const others = d.valid_answers.filter(a => a !== answer);
    fb.innerHTML = '✓ Đúng rồi.' +
      (others.length ? `<span class="alt">cũng đúng: ${others.join(', ')}</span>` : '');
    fb.className = 'feedback correct';
  } else {
    const [first, ...rest] = d.valid_answers;
    fb.innerHTML = `✗ Đáp án: <b>${first}</b>` +
      (rest.length ? `<span class="alt">cũng đúng: ${rest.join(', ')}</span>` : '');
    fb.className = 'feedback wrong';
  }

  $('score').textContent = d.score;
  $('total').textContent = d.total;
  $('nextBtn').disabled = false;
}

$('nextBtn').addEventListener('click', loadQuestion);
$('resetBtn').addEventListener('click', async () => {
  await fetch('/reset', {method:'POST'});
  $('score').textContent = '0';
  $('total').textContent = '0';
  loadQuestion();
});

// phím tắt: 1-4 chọn đáp án, Enter / Space cho câu tiếp
document.addEventListener('keydown', e => {
  if (['1','2','3','4'].includes(e.key)){
    const opts = document.querySelectorAll('.opt');
    const i = parseInt(e.key,10) - 1;
    if (opts[i] && !opts[i].disabled) opts[i].click();
  } else if ((e.key === 'Enter' || e.key === ' ') && !$('nextBtn').disabled){
    e.preventDefault();
    $('nextBtn').click();
  }
});

loadQuestion();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
