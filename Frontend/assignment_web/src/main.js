// ฟังก์ชันจัดการชื่อไฟล์
function handleFileSelect(input, displayId) {
    const displayElement = document.getElementById(displayId);
    if (input.files.length > 0) {
        displayElement.innerText = "เลือกไฟล์แล้ว: " + input.files[0].name;
        displayElement.style.color = "var(--secondary)";
    }
}

// ฟังก์ชันอัปโหลดไฟล์
async function uploadFile(inputId) {
    const fileInput = document.getElementById(inputId);
    const file = fileInput.files[0];

    if (!file) {
        alert("กรุณาเลือกไฟล์ก่อน!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
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
function logout() {
    if (confirm("ต้องการออกจากระบบ?")) {
        window.location.href = "index.html";
    }
}