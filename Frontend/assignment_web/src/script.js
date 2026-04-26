// ===========================
// script.js — App Logic
// ไม่มี data อยู่ที่นี่
// data ทั้งหมดอยู่ใน data/tasks.js
// ===========================

// State
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
// Page Navigation
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
// Logout
// ===========================
function logout() {
  sessionStorage.removeItem('isLoggedIn');
  window.location.href = 'login.html';
}

// ===========================
// LINE Popup
// ===========================
function openLinePopup() {
  document.getElementById('line-overlay').classList.add('open');
  document.getElementById('line-popup').classList.add('open');
}

function closeLinePopup() {
  document.getElementById('line-overlay').classList.remove('open');
  document.getElementById('line-popup').classList.remove('open');
}

// ===========================
// Init
// ===========================
renderTasks();
