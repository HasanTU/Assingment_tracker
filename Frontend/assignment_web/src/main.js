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

    // Scroll to top
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
        // Student: Only Dashboard (Submission)
        navDashboard.classList.remove('hidden');
        navCreation.classList.add('hidden');
        navTracker.classList.add('hidden');
        navHelp.classList.add('hidden');
        userName.innerText = 'ปิยบุตร เก่งกาจ (นักศึกษา)';
        dashboardTitle.innerText = 'สวัสดี, ปิยบุตร';
        navigateTo('dashboard');
    } else if (role === 'teacher') {
        // Teacher: Creation and Tracker
        navDashboard.classList.add('hidden');
        navCreation.classList.remove('hidden');
        navTracker.classList.remove('hidden');
        navHelp.classList.add('hidden');
        userName.innerText = 'สมชาย ใจดี (อาจารย์)';
        navigateTo('creation');
    }
}

// Modal Handling
function openSubmitModal(assignmentName) {
    const modal = document.getElementById('submit-modal');
    if (modal) {
        modal.classList.remove('hidden');
        // You could update modal content here based on assignmentName
    }
}

function closeSubmitModal() {
    const modal = document.getElementById('submit-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// File Upload Handling
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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Start at login
    navigateTo('login');
    
    // Add some interactivity to buttons that don't have it yet
    const buttons = document.querySelectorAll('button:not([onclick])');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log('Button clicked:', btn.innerText);
        });
    });
});

// Expose functions to global scope for inline onclick
window.navigateTo = navigateTo;
window.loginAs = loginAs;
window.openSubmitModal = openSubmitModal;
window.closeSubmitModal = closeSubmitModal;
window.handleFileSelect = handleFileSelect;
