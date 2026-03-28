// Global state
let currentUserRole = null;

// Navigation Logic
function navigateTo(pageId) {
    const pages = ['login', 'dashboard', 'tracker', 'creation'];
    const loginPage = document.getElementById('login-page');
    const mainLayout = document.getElementById('main-layout');

    // Hide all pages
    pages.forEach(p => {
        const page = document.getElementById(`${p}-page`);
        if (page) page.classList.remove('active');
    });

    // Handle Login vs Main Layout
    if (pageId === 'login') {
        loginPage.classList.add('active');
        loginPage.classList.remove('hidden');
        mainLayout.classList.add('hidden');
        currentUserRole = null;
    } else {
        loginPage.classList.remove('active');
        loginPage.classList.add('hidden');
        mainLayout.classList.remove('hidden');

        const targetPage = document.getElementById(`${pageId}-page`);
        if (targetPage) targetPage.classList.add('active');

        // Update nav links
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(pageId)) {
                link.classList.add('active');
            }
        });
    }

    window.scrollTo(0, 0);
}

// Role-based Login
function loginAs(role) {
    currentUserRole = role;

    const navDashboard = document.getElementById('nav-dashboard');
    const navCreation = document.getElementById('nav-creation');
    const navTracker = document.getElementById('nav-tracker');
    const navHelp = document.getElementById('nav-help');
    const userName = document.querySelector('.user-profile .label-sm');
    const dashboardTitle = document.querySelector('#dashboard-page h1');

    if (role === 'student') {
        navDashboard.classList.remove('hidden');
        navCreation.classList.add('hidden');
        navTracker.classList.add('hidden');
        navHelp.classList.add('hidden');

        if (userName) userName.innerText = 'ปิยบุตร เก่งกาจ (นักศึกษา)';
        if (dashboardTitle) dashboardTitle.innerText = 'สวัสดี, ปิยบุตร';

        navigateTo('dashboard');

    } else if (role === 'teacher') {
        navDashboard.classList.add('hidden');
        navCreation.classList.remove('hidden');
        navTracker.classList.remove('hidden');
        navHelp.classList.add('hidden');

        if (userName) userName.innerText = 'สมชาย ใจดี (อาจารย์)';

        navigateTo('creation');
    }
}

// Modal Handling
function openSubmitModal() {
    const modal = document.getElementById('submit-modal');
    if (modal) modal.classList.remove('hidden');
}

function closeSubmitModal() {
    const modal = document.getElementById('submit-modal');
    if (modal) modal.classList.add('hidden');
}

// File Upload Handling (UI)
function handleFileSelect(input, displayId) {
    const displayElement = document.getElementById(displayId);

    if (input.files && input.files.length > 0) {
        const fileName = input.files[0].name;
        displayElement.innerText = `เลือกไฟล์แล้ว: ${fileName}`;
        displayElement.style.color = 'var(--primary)';
        displayElement.style.fontWeight = '700';
    } else {
        displayElement.innerText = 'ลากไฟล์มาวางที่นี่ หรือคลิกเพื่อเลือกไฟล์';
        displayElement.style.color = 'inherit';
        displayElement.style.fontWeight = 'inherit';
    }
}

// ✅ FIXED Upload File (สำคัญ)
function uploadFile() {
    const fileInput = document.getElementById("assignment-file");
    const file = fileInput.files[0];

    if (!file) {
        alert("กรุณาเลือกไฟล์ก่อน");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log("Upload success:", data);
        alert("อัปโหลดสำเร็จ");
    })
    .catch(err => {
        console.error(err);
        alert("อัปโหลดล้มเหลว");
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    navigateTo('login');

    const buttons = document.querySelectorAll('button:not([onclick])');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log('Button clicked:', btn.innerText);
        });
    });
});

// Expose to global
window.navigateTo = navigateTo;
window.loginAs = loginAs;
window.openSubmitModal = openSubmitModal;
window.closeSubmitModal = closeSubmitModal;
window.handleFileSelect = handleFileSelect;
window.uploadFile = uploadFile;