// ===========================
// 5 เมฆ — Data
// ===========================
var tasks = [
  { id: 1, name: 'Assignment 5',    course: 'CS222', due: '1 Apr 2026',  status: 'late',    desc: 'จงทำการออกแบบเกมที่คุณได้เล่นไปล่าสุดแล้วนำมาส่งผมด้วยนะครับ' },
  { id: 2, name: 'Assignment 3',    course: 'CS232', due: '7 Apr 2026',  status: 'pending', desc: 'วิเคราะห์ความซับซ้อนของ Sorting Algorithms อย่างน้อย 3 แบบ พร้อมตัวอย่าง code' },
  { id: 3, name: 'Lab Report 2',    course: 'CS251', due: '10 Apr 2026', status: 'pending', desc: 'จัดทำรายงานผลการทดลองเรื่อง Process Scheduling ในระบบปฏิบัติการ' },
  { id: 4, name: 'Quiz 4',          course: 'CS271', due: '12 Apr 2026', status: 'pending', desc: 'ทำแบบทดสอบบทที่ 4 เรื่อง Network Layer ผ่านระบบ MS Teams' },
  { id: 5, name: 'Project Phase 1', course: 'CS242', due: '2 Apr 2026',  status: 'done',    desc: 'ส่ง proposal โปรเจกต์ Database พร้อม ER Diagram' },
  { id: 6, name: 'Homework 6',      course: 'CS222', due: '2 Apr 2026',  status: 'done',    desc: 'แก้โจทย์ Graph Theory ข้อ 1-10 จากใบงานที่แจก' },
  { id: 7, name: 'Assignment 2',    course: 'EL395', due: '28 Mar 2026', status: 'done',    desc: 'เขียนรายงานสรุปบทความวิชาการ 1 หน้า A4' },
  { id: 8, name: 'Lab 3',           course: 'CS217', due: '25 Mar 2026', status: 'done',    desc: 'ทดลองและรายงานผลการทดลองวงจรดิจิทัลพื้นฐาน' },
];

var statsByAll = { done: 23, pending: 15, late: 3 };
var statsByCourse = {
  'CS232': { done: 6, pending: 1, late: 0 },
  'CS251': { done: 4, pending: 2, late: 0 },
  'CS222': { done: 8, pending: 0, late: 1 },
  'CS271': { done: 2, pending: 1, late: 0 },
  'CS242': { done: 1, pending: 0, late: 0 },
  'CS217': { done: 1, pending: 0, late: 0 },
  'EL395': { done: 1, pending: 0, late: 0 },
};

// ===========================
// State
// ===========================
var currentCourse = 'all';
var completedOpen = false;

// ===========================
// Helpers
// ===========================
function getDotClass(s) {
  return s === 'late' ? 'dot-late' : s === 'done' ? 'dot-done' : 'dot-pending';
}

function getBadgeClass(s) {
  return s === 'late' ? 'badge-late' : s === 'done' ? 'badge-done' : 'badge-pending';
}

function getBadgeText(s) {
  return s === 'late' ? 'ส่งล่าช้า' : s === 'done' ? 'ส่งแล้ว' : 'ยังไม่ส่ง';
}

function makeCard(t) {
  return (
    '<div class="task-card" onclick="showDetail(' + t.id + ')">' +
      '<div class="task-card-left">' +
        '<div class="dot ' + getDotClass(t.status) + '"></div>' +
        '<div>' +
          '<div class="task-name">' + t.name + '</div>' +
          '<div class="task-sub">Due: ' + t.due + ' &nbsp;&middot;&nbsp; ' + t.course + '</div>' +
        '</div>' +
      '</div>' +
      '<span class="badge ' + getBadgeClass(t.status) + '">' + getBadgeText(t.status) + '</span>' +
    '</div>'
  );
}

// ===========================
// Render Tasks
// ===========================
function renderTasks() {
  var filtered = currentCourse === 'all'
    ? tasks
    : tasks.filter(function(t) { return t.course === currentCourse; });

  var active = filtered.filter(function(t) { return t.status !== 'done'; });
  var done   = filtered.filter(function(t) { return t.status === 'done'; });

  document.getElementById('task-list').innerHTML      = active.map(makeCard).join('');
  document.getElementById('completed-list').innerHTML = done.map(makeCard).join('');

  var s = currentCourse === 'all'
    ? statsByAll
    : (statsByCourse[currentCourse] || { done: 0, pending: 0, late: 0 });

  document.getElementById('stat-done').textContent    = s.done;
  document.getElementById('stat-pending').textContent = s.pending;
  document.getElementById('stat-late').textContent    = s.late;
}

// ===========================
// Filter by Course
// ===========================
function filterCourse(course, el) {
  currentCourse = course;

  document.querySelectorAll('.sbi').forEach(function(b) { b.classList.remove('active'); });
  el.classList.add('active');

  document.getElementById('topbar-title').textContent =
    course === 'all' ? 'All Task assignment' : course + ' — Task assignment';

  completedOpen = false;
  document.getElementById('completed-list').style.display = 'none';
  document.getElementById('comp-arrow').textContent = '▼';

  renderTasks();
}

// ===========================
// Completed Toggle
// ===========================
function toggleCompleted() {
  completedOpen = !completedOpen;
  document.getElementById('completed-list').style.display = completedOpen ? 'block' : 'none';
  document.getElementById('comp-arrow').textContent = completedOpen ? '▲' : '▼';
}

// ===========================
// Task Detail
// ===========================
function showDetail(id) {
  var t = tasks.find(function(x) { return x.id === id; });
  if (!t) return;

  document.getElementById('d-title').textContent  = t.name;
  document.getElementById('d-course').textContent = t.course;
  document.getElementById('d-desc').textContent   = t.desc;

  var due = document.getElementById('d-due');
  due.textContent = 'Due: ' + t.due;
  due.className   = 'detail-due' + (t.status === 'late' ? ' urgent' : '');

  var badge = document.getElementById('d-badge');
  badge.textContent = getBadgeText(t.status);
  badge.className   = 'badge ' + getBadgeClass(t.status);

  document.getElementById('page-list').classList.remove('active');
  document.getElementById('page-detail').classList.add('active');
}

function showList() {
  document.getElementById('page-detail').classList.remove('active');
  document.getElementById('page-list').classList.add('active');
}

// ===========================
// Init
// ===========================
renderTasks();
