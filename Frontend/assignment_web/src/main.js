// ฟังก์ชันจัดการชื่อไฟล์
function handleFileSelect(input, displayId) {
    const displayElement = document.getElementById(displayId);
    if (input.files.length > 0) {
        displayElement.innerText = "เลือกไฟล์แล้ว: " + input.files[0].name;
        displayElement.style.color = "var(--secondary)";
    }
}

// ฟังก์ชันอัปโหลดไฟล์
async function uploadFile(inputId, path) {
    const fileInput = document.getElementById(inputId);
    const file = fileInput.files[0];

    if (!file) {
        alert("กรุณาเลือกไฟล์ก่อน!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("path", path);
    try {
        const response = await fetch("http://127.0.0.1:5000/api/upload", {
            method: "POST",
            body: formData,
            credentials: "include"
        });
        if (response.ok) {
            alert("อัปโหลดสำเร็จ!");
        } else {
            alert("อัปโหลดล้มเหลว (เช็ค Backend)");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("ไม่สามารถติดต่อเซิร์ฟเวอร์ได้");
    }
}

// ฟังก์ชัน Logout
async function logout() {
    if (confirm("ต้องการออกจากระบบ?")) {
        try {
            const response = await fetch("http://127.0.0.1:5000/api/logout", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({})
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "error");
            }
            
            localStorage.removeItem("user_info");
            window.location.href = "index.html";

            alert("Logout!");
        } catch (err) {
            console.error(err);
            alert("Logout ไม่สำเร็จ");
        }
    }
}



async function initAuth() {
    const currentPage = window.location.pathname;
    const isLoginPage = currentPage.includes("index.html") || currentPage === "/" || currentPage.endsWith("login.html");

    const cachedUser = localStorage.getItem('user_info');
    
 
    if (isLoginPage) {
        if (cachedUser) {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/me', {
                    method: "GET",
                    credentials: "include" 
                });

                if (response.ok) {
                    const user = await response.json();
                    window.location.href = user.role === "teacher" ? "teacher.html" : "student.html";
                    return;
                }
            } catch (e) { localStorage.removeItem('user_info'); }
        }
        return;
    }


    try {
        const response = await fetch('http://127.0.0.1:5000/api/me', {
            method: "GET",
            credentials: "include"
        });

        if (response.ok) {
            const user = await response.json();
            localStorage.setItem('user_info', JSON.stringify(user));
            

            if (user.role === "student" && currentPage.includes("teacher.html")) {
                alert("ผิดหน้า");
                window.location.href = "student.html";
            } else if (user.role === "teacher" && currentPage.includes("student.html")) {
                alert("ผิดหน้า");
                window.location.href = "teacher.html";
            }
            

            if (typeof renderUserUI === 'function') renderUserUI(user);

        } else {
            localStorage.removeItem('user_info');
            window.location.href = "index.html";
        }
    } catch (error) {
        console.error("Connection Error");
        window.location.href = "index.html";
    }
}

document.addEventListener('DOMContentLoaded', initAuth);


function renderUserUI(user) {
    const userNameEl = document.getElementById("display-name-user");

    if(!userNameEl) return

    if (user.role === "student") {
        userNameEl.innerText = user.first_name + " " + user.last_name + " (นักศึกษา)"

        const usernameBoard = document.getElementById("display-dashboard-name");
        if(usernameBoard) usernameBoard.innerHTML = "สวัสดี, " + user.first_name
    } else if (user.role === "teacher") {
        userNameEl.innerText = "อ. "+ user.first_name + " " + user.last_name + " (อาจารย์)"
    }
}