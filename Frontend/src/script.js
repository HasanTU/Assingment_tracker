// ===========================
// script.js — App Logic
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
// Render Functions
// ===========================
function renderCourses(){
  const sidebar = document.querySelector(".sidebar-courses-list");
  // ล้างรายการเดิมก่อน (ยกเว้นหัวข้อ)
  const existingItems = sidebar.querySelectorAll(".sbi:not(.active)");
  existingItems.forEach(item => item.remove());

  courses.forEach(course => {
    const div = document.createElement("div");
    div.className = "sbi";
    div.onclick = function () { filterCourse(course, this); };

    const dot = document.createElement("div");
    dot.className = "sbi-dot";

    div.appendChild(dot);
    div.appendChild(document.createTextNode(course));
    sidebar.appendChild(div);
  });
}

function renderTasks() {
  var filtered = currentCourse === 'all'
    ? tasks
    : tasks.filter(function(t) { return t.course === currentCourse; });

  var active = filtered.filter(function(t) { return t.status !== 'done'; });
  var done   = filtered.filter(function(t) { return t.status === 'done'; });

  document.getElementById('task-list').innerHTML      = active.map(makeCard).join('');
  document.getElementById('completed-list').innerHTML = done.map(makeCard).join('');

  var statsByAll = tasks.reduce(function(acc, t) {
    acc[t.status] = (acc[t.status] || 0) + 1;
    return acc;
  }, { done: 0, pending: 0, late: 0 });

  var statsByCourse = tasks.reduce(function(acc, t) {
    if (!acc[t.course]) acc[t.course] = { done: 0, pending: 0, late: 0 };
    acc[t.course][t.status] = (acc[t.course][t.status] || 0) + 1;
    return acc;
  }, {});

  var s = currentCourse === 'all'
    ? statsByAll
    : (statsByCourse[currentCourse] || { done: 0, pending: 0, late: 0 });

  document.getElementById('stat-done').textContent    = s.done;
  document.getElementById('stat-pending').textContent = s.pending;
  document.getElementById('stat-late').textContent    = s.late;
}

// ===========================
// Interaction Functions
// ===========================
function filterCourse(course, el) {
  showList();
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

function toggleCompleted() {
  completedOpen = !completedOpen;
  document.getElementById('completed-list').style.display = completedOpen ? 'block' : 'none';
  document.getElementById('comp-arrow').textContent = completedOpen ? '▲' : '▼';
}

function showDetail(id) {
  var t = tasks.find(function(x) { return x.id === id; });
  if (!t) return;

  document.getElementById('d-title').textContent  = t.name;
  document.getElementById('d-course').textContent = t.course;
  
  var container = document.getElementById('d-desc');
  container.innerHTML = t.desc;

  var due = document.getElementById('d-due');
  due.textContent = 'Due: ' + t.due;
  due.className   = 'detail-due' + (t.status === 'late' ? ' urgent' : '');

  var badge = document.getElementById('d-badge');
  badge.textContent = getBadgeText(t.status);
  badge.className   = 'badge ' + getBadgeClass(t.status);

  const link = document.querySelector("#d-assignment-url a");
  link.href = t.source_url;
  link.textContent = t.source_url;

  document.getElementById('page-list').classList.remove('active');
  document.getElementById('page-detail').classList.add('active');
}

function showList() {
  document.getElementById('page-detail').classList.remove('active');
  document.getElementById('page-list').classList.add('active');
}

// ===========================
// Popup Functions
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
// Auth & Logout
// ===========================
async function logout() {
  try {
    const response = await fetch(`${APP.CONFIG.BACKEND_API_URL}/logout`, {
        method: "POST",
        credentials: "include"
    });

    if (response.ok) {
        sessionStorage.clear();
        window.location.replace("index.html");
    } else {
        console.error("Logout failed");
    }
  } catch (err) {
      console.error("Error during logout:", err);
      sessionStorage.clear();
      window.location.replace("index.html");
  }
}

// ===========================
// Init (Combined)
// ===========================
document.addEventListener("DOMContentLoaded", async () => {
  // 1. Check Auth
  if (sessionStorage.getItem('isLoggedIn') !== 'true') {
    window.location.replace('index.html');
    return;
  }

  // 2. Load User Data
  const userStr = sessionStorage.getItem("user");
  if (userStr) {
    try {
      const userData = JSON.parse(userStr);
      // แสดงชื่อใน Topbar
      if (userData.display_name) {
        const names = userData.display_name.trim().split(/\s+/);
        document.getElementById("display-firstname").textContent = names[0] || userData.username;
        document.getElementById("display-lastname").textContent = names[1] || "";
      }
      // อัปเดต username/รหัสนักศึกษา (ถ้ามี)
      const usernameSpan = document.querySelector(".topbar-name span");
      if (usernameSpan) usernameSpan.textContent = userData.username || "--";
      
    } catch (e) {
      console.error("User data error", e);
    }
  }

  // 3. Initial Render
  if (typeof courses !== 'undefined') renderCourses();
  if (typeof tasks !== 'undefined') renderTasks();
});