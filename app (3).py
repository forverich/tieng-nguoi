"""
Trắc nghiệm tiếng khỉ — tiếng người (phiên bản Streamlit Cloud)
Chạy:   pip install streamlit
        streamlit run app.py
"""
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tiếng khỉ — Tiếng người",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Ẩn chrome mặc định của Streamlit để cho giao diện chiếm trọn
st.markdown(
    """
    <style>
      #MainMenu, footer, header { visibility: hidden; }
      .block-container { padding: 0 !important; max-width: 100% !important; }
      [data-testid="stAppViewContainer"] { background: #f4ecd8; }
      iframe { border: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# (tiếng khỉ, [đáp án tiếng người chấp nhận])
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

vocab_json = json.dumps(VOCAB, ensure_ascii=False)

HTML = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
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
    --accent:#8b2e2e;
    --accent-soft:#c2786e;
    --green:#3d6b3a;
    --green-soft:#aac49a;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{height:auto;min-height:100%;}
  body{
    font-family:"EB Garamond", Georgia, serif;
    color:var(--ink);
    background:
      radial-gradient(ellipse at 20% 10%, rgba(255,255,255,.5), transparent 50%),
      radial-gradient(ellipse at 80% 90%, rgba(139,46,46,.06), transparent 60%),
      var(--paper);
    min-height:100vh;
    display:flex; align-items:flex-start; justify-content:center;
    padding:30px 16px 40px;
    position:relative;
  }
  body::before{
    content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
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
    padding: 38px 44px 32px;
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
    padding-bottom:16px; margin-bottom:22px;
  }
  .masthead .title{
    font-family:"Cormorant Garamond", serif;
    font-weight:700;
    font-size: clamp(26px, 4.4vw, 36px);
    letter-spacing:-.01em; line-height:1;
  }
  .masthead .title em{ font-style: italic; color: var(--accent); font-weight:600; }
  .masthead .meta{
    font-family:"JetBrains Mono", monospace;
    font-size:11px; letter-spacing:.14em; text-transform:uppercase;
    color:var(--ink-soft); text-align:right; line-height:1.6;
  }
  .scorebar{
    display:flex; justify-content:space-between; align-items:center;
    font-family:"JetBrains Mono", monospace; font-size:12px;
    color:var(--ink-soft); letter-spacing:.08em;
    padding:8px 0 18px;
    border-bottom:1px dashed var(--rule); margin-bottom:20px;
  }
  .scorebar b{ color:var(--ink); font-weight:500; }
  .scorebar .right{ text-align:right; }
  .prompt-label{
    font-family:"JetBrains Mono", monospace;
    font-size:11px; letter-spacing:.22em; text-transform:uppercase;
    color:var(--accent); margin-bottom:6px; text-align:center;
  }
  .question{
    text-align:center;
    font-family:"Cormorant Garamond", serif;
    font-style: italic; font-weight:500;
    font-size: clamp(36px, 6.4vw, 58px);
    line-height:1.05;
    padding: 14px 12px 22px;
    color: var(--ink);
  }
  .question::before, .question::after{
    content:"❧"; color: var(--accent-soft); font-style:normal;
    display:block; font-size:13px; letter-spacing:.5em; margin:4px 0;
  }
  .options{ display:grid; gap:10px; margin-top:4px; }
  .opt{
    appearance:none; cursor:pointer; text-align:left;
    font-family:"EB Garamond", serif; font-size:18px;
    color:var(--ink); background:transparent;
    border:1px solid var(--rule); border-left:3px solid var(--rule);
    padding:13px 17px; border-radius:1px;
    transition: background .15s, border-color .15s, transform .08s;
    display:flex; align-items:baseline; gap:14px;
  }
  .opt .letter{
    font-family:"JetBrains Mono", monospace;
    font-size:11px; letter-spacing:.1em;
    color:var(--ink-soft); min-width:18px;
  }
  .opt:hover:not(:disabled){
    background:rgba(139,46,46,.05); border-left-color:var(--accent);
  }
  .opt:active:not(:disabled){ transform: translateY(1px); }
  .opt:disabled{ cursor:default; }
  .opt.correct{
    background:rgba(61,107,58,.12);
    border-color:var(--green); border-left-color:var(--green); color:var(--green);
  }
  .opt.correct .letter{ color:var(--green); }
  .opt.wrong{
    background:rgba(139,46,46,.10);
    border-color:var(--accent); border-left-color:var(--accent); color:var(--accent);
    text-decoration: line-through; text-decoration-color: var(--accent-soft);
  }
  .opt.wrong .letter{ color:var(--accent); }
  .feedback{
    margin-top:18px; min-height:24px;
    font-style:italic; font-size:16px; text-align:center; color: var(--ink-soft);
  }
  .feedback.correct{ color: var(--green); }
  .feedback.wrong  { color: var(--accent); }
  .feedback .alt{
    display:block; font-size:13px; margin-top:4px;
    color:var(--ink-soft); font-style:normal;
    font-family:"JetBrains Mono", monospace; letter-spacing:.04em;
  }
  .actions{
    display:flex; justify-content:space-between; align-items:center;
    margin-top:22px; padding-top:16px; border-top:1px solid var(--rule);
  }
  .next{
    appearance:none; cursor:pointer;
    font-family:"Cormorant Garamond", serif; font-weight:600;
    font-size:16px; letter-spacing:.02em;
    background:var(--ink); color:var(--paper);
    border:none; padding:11px 20px; border-radius:1px;
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
    text-align:center; margin-top:16px;
    font-family:"JetBrains Mono", monospace;
    font-size:10px; letter-spacing:.18em; text-transform:uppercase;
    color:var(--ink-soft); opacity:.7;
  }
  @media (max-width:520px){
    body{ padding:20px 10px 30px; }
    .sheet{ padding:26px 20px 22px; }
    .masthead{ flex-direction:column; align-items:flex-start; gap:8px;}
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
const VOCAB = __VOCAB_JSON__;
const $ = id => document.getElementById(id);
let seen = [];
let score = 0, total = 0;
let currentValid = [];
let answered = false;

function rand(n){ return Math.floor(Math.random()*n); }
function shuffle(a){ for(let i=a.length-1;i>0;i--){ const j=rand(i+1); [a[i],a[j]]=[a[j],a[i]]; } return a; }

function pickQuestion(){
  if (seen.length >= VOCAB.length) seen = [];
  const available = VOCAB.filter(v => !seen.includes(v[0]));
  const pair = available[rand(available.length)];
  seen.push(pair[0]);
  const [khi, valid] = pair;
  const correct = valid[rand(valid.length)];
  const others = VOCAB.filter(v => v[0] !== khi);
  const distractors = [];
  let attempts = 0;
  while (distractors.length < 3 && attempts < 200){
    attempts++;
    const p = others[rand(others.length)];
    const cand = p[1][rand(p[1].length)];
    if (!valid.includes(cand) && !distractors.includes(cand)) distractors.push(cand);
  }
  const options = shuffle([correct, ...distractors]);
  currentValid = valid;
  return { question: khi, options, remaining: VOCAB.length - seen.length };
}

function loadQuestion(){
  answered = false;
  $('feedback').textContent = '';
  $('feedback').className = 'feedback';
  $('nextBtn').disabled = true;
  $('options').innerHTML = '';

  const q = pickQuestion();
  $('question').textContent = q.question;
  $('remaining').textContent = q.remaining;
  $('totalvocab').textContent = VOCAB.length;

  const letters = ['A','B','C','D','E','F'];
  q.options.forEach((opt, i) => {
    const b = document.createElement('button');
    b.className = 'opt'; b.type = 'button';
    b.innerHTML = `<span class="letter">${letters[i]}</span><span>${opt}</span>`;
    b.addEventListener('click', () => submit(opt, b));
    $('options').appendChild(b);
  });
}

function submit(answer, btn){
  if (answered) return;
  answered = true;

  const isCorrect = currentValid.includes(answer);
  total++; if (isCorrect) score++;

  document.querySelectorAll('.opt').forEach(b => {
    b.disabled = true;
    const label = b.querySelector('span:last-child').textContent;
    if (currentValid.includes(label)) b.classList.add('correct');
    else if (b === btn) b.classList.add('wrong');
  });

  const fb = $('feedback');
  if (isCorrect){
    const others = currentValid.filter(a => a !== answer);
    fb.innerHTML = '✓ Đúng rồi.' +
      (others.length ? `<span class="alt">cũng đúng: ${others.join(', ')}</span>` : '');
    fb.className = 'feedback correct';
  } else {
    const [first, ...rest] = currentValid;
    fb.innerHTML = `✗ Đáp án: <b>${first}</b>` +
      (rest.length ? `<span class="alt">cũng đúng: ${rest.join(', ')}</span>` : '');
    fb.className = 'feedback wrong';
  }

  $('score').textContent = score;
  $('total').textContent = total;
  $('nextBtn').disabled = false;
}

$('nextBtn').addEventListener('click', loadQuestion);
$('resetBtn').addEventListener('click', () => {
  score = 0; total = 0; seen = [];
  $('score').textContent = '0';
  $('total').textContent = '0';
  loadQuestion();
});

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
""".replace("__VOCAB_JSON__", vocab_json)

components.html(HTML, height=950, scrolling=True)
