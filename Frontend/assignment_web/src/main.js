// ฟังก์ชัน redirect ไปหน้าที่ถูกต้อง
async function protectPage() {
    const path = window.location.pathname;
    if (path.includes("index.html") || path === "/") {
        console.log("อยู่ในหน้า Login");
        return; 
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/verify-role', {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            // ถ้า Token เสีย หรือไม่มีสิทธิ์ ให้เด้งกลับหน้า Login
            window.location.href = "index.html";
            return;
        }

        const data = await response.json();
        
        const currentPage = window.location.pathname;
        if (data.role === "student" && currentPage.includes("teacher.html")) {
            alert("ผิดหน้า");
            window.location.href = "student.html";
        }else if(data.role === "teacher" && currentPage.includes("student.html")){
            alert("ผิดหน้า");
            window.location.href = "teacher.html";
        }

    } catch (error) {
        window.location.href = "index.html";
    }
}

protectPage();


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
            
            window.location.href = "index.html";

            alert("Logout!");
        } catch (err) {
            console.error(err);
            alert("Logout ไม่สำเร็จ");
        }
    }
}