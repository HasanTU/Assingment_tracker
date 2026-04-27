document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("auth-btn-login");
    const emailInput = document.getElementById("login-email");
    const passwordInput = document.getElementById("login-password");
    const errorEl = document.getElementById('login-error');

    btnLogin.addEventListener("click", async () => {
        const username = emailInput.value.trim();
        const password = passwordInput.value;

        if (!username || !password) {
            errorEl.textContent = 'กรุณากรอกข้อมูลให้ครบถ้วน';
            errorEl.style.display = 'block';
            return;
        }

        btnLogin.disabled = true;
        btnLogin.textContent = "กำลังตรวจสอบ...";
        errorEl.style.display = 'none';

        try {
            const response = await fetch(`${APP.CONFIG.BACKEND_API_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
                credentials: "include"
            });

            const data = await response.json();

            if (response.ok) {
                // บันทึก Session
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem("user", JSON.stringify({
                    username: data.username,
                    display_name: data.display_name
                }));

                // ย้ายไปหน้า student.html
                window.location.replace("student.html"); 
            } else {
                errorEl.textContent = data.message || 'รหัสผิดหรือเข้าสู่ระบบไม่ได้';
                errorEl.style.display = 'block';
                btnLogin.disabled = false;
                btnLogin.textContent = "ยืนยัน";
            }
        } catch (err) {
            console.error("Error:", err);
            errorEl.textContent = 'ติดต่อเซิร์ฟเวอร์ไม่ได้';
            errorEl.style.display = 'block';
            btnLogin.disabled = false;
            btnLogin.textContent = "ยืนยัน";
        }
    });
});
// async function handleLogin(e) {
//     e.preventDefault();
//     e.stopPropagation();

//     console.log("Button clicked! Attempting to login...");

//     var username = document.getElementById('login-email').value.trim();
//     var password = document.getElementById('login-password').value;
//     var errorEl  = document.getElementById('login-error');

//     if (!username || !password) {
//         errorEl.textContent = 'กรุณากรอกรหัสนักศึกษาและรหัสผ่าน';
//         errorEl.style.display = 'block';
//         return;
//     }

//   // ตรงนี้ backend เชื่อม API ได้เลย
//     try {
//         console.log("Starting fetch..."); // เพิ่มบรรทัดนี้
//         const response = await fetch(`${APP.CONFIG.BACKEND_API_URL}/login`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ username, password }),
//             credentials: "include"
//         });

//         console.log("Response received:", response.status); // เพิ่มบรรทัดนี้
//         const data = await response.json();
//         console.log("Data parsed:", data); // เพิ่มบรรทัดนี้

//         if (response.ok) {
//             sessionStorage.setItem('isLoggedIn', 'true');
//             errorEl.style.display = 'none';
//             if (sessionStorage.getItem('isLoggedIn') === 'true') {
//                 //window.location.href = "index.html";
//             } else {
//                 alert('เกิดข้อผิดพลาดในการบันทึก Session');
//             }
            
//             // window.location.href = "index.html";
//         } else {
//             errorEl.textContent = 'รหัสนักศึกษาหรือรหัสผ่านผ่านผิด';
//             errorEl.style.display = 'block';
            
//         }
//     } catch (err) {
//         console.error("Fetch Error Detail:", err); // ดู Error แบบละเอียด
//         errorEl.textContent = 'ติดต่อ Server ไม่ได้';
//         errorEl.style.display = 'block';
        
//     }


//     // ตอนนี้ใช้ dummy check ก่อน
//     // errorEl.style.display = 'none';
//     // sessionStorage.setItem('isLoggedIn', 'true');
//     //window.location.href = 'index.html';
// }

// document.addEventListener("DOMContentLoaded", () => {
//     const btnLogin = document.getElementById("auth-btn-login");

//     // ตรวจสอบเบื้องต้นว่าเจอตัวแปรไหม
//     console.log("Config URL:", APP.CONFIG.BACKEND_API_URL);

//     if (btnLogin) {
//         btnLogin.addEventListener("click", async (e) => {
//             e.preventDefault();
//             e.stopPropagation();

//             console.log("Button clicked! Attempting to login...");

//             var username = document.getElementById('login-email').value.trim();
//             var password = document.getElementById('login-password').value;
//             var errorEl  = document.getElementById('login-error');

//             if (!username || !password) {
//                 errorEl.textContent = 'กรุณากรอกรหัสนักศึกษาและรหัสผ่าน';
//                 errorEl.style.display = 'block';
//                 return;
//             }

//         // ตรงนี้ backend เชื่อม API ได้เลย
//             try {
//                 console.log("Starting fetch..."); // เพิ่มบรรทัดนี้
//                 const response = await fetch(`${APP.CONFIG.BACKEND_API_URL}/login`, {
//                     method: "POST",
//                     headers: { "Content-Type": "application/json" },
//                     body: JSON.stringify({ username, password }),
//                     credentials: "include"
//                 });

//                 console.log("Response received:", response.status); // เพิ่มบรรทัดนี้
//                 const data = await response.json();
//                 console.log("Data parsed:", data); // เพิ่มบรรทัดนี้

//                 if (response.ok) {
//                     sessionStorage.setItem('isLoggedIn', 'true');
//                     errorEl.style.display = 'none';
//                     if (sessionStorage.getItem('isLoggedIn') === 'true') {
//                         //window.location.href = "index.html";
//                     } else {
//                         alert('เกิดข้อผิดพลาดในการบันทึก Session');
//                     }
                    
//                     // window.location.href = "index.html";
//                 } else {
//                     errorEl.textContent = 'รหัสนักศึกษาหรือรหัสผ่านผ่านผิด';
//                     errorEl.style.display = 'block';
                    
//                 }
//             } catch (err) {
//                 console.error("Fetch Error Detail:", err); // ดู Error แบบละเอียด
//                 errorEl.textContent = 'ติดต่อ Server ไม่ได้';
//                 errorEl.style.display = 'block';
                
//             }


//             // ตอนนี้ใช้ dummy check ก่อน
//             // errorEl.style.display = 'none';
//             // sessionStorage.setItem('isLoggedIn', 'true');
//             //window.location.href = 'index.html';
//         }); // ปิด btnLogin.addEventListener
//     } else {
//         console.error("หาปุ่ม btn-login ไม่เจอ!");
//     }
// }); 


//กด Enter เพื่อ login ได้เลย
// document.addEventListener('keydown', (e) => {
//     if (e.key === 'Enter') {
//         e.preventDefault();
//         e.stopPropagation();
//         const btn = document.getElementById("auth-btn-login");
//         // สั่งให้ปุ่มถูกคลิก (ซึ่งจะไปเรียก logic ด้านบนที่มี preventDefault เรียบร้อยแล้ว)
//         if (btn) btn.click();
//     }
// });