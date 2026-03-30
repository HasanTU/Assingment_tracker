async function uploadAssignmentFile(data){
    // const assignmentId = data.assignment_id
    // const courseId = data.course_id

    // const dict = {
    //     "assignment_id":assignmentId,
    //     "course_id":courseId
    // }

    uploadFile('teacher-file', 'teacher', "/assignment", data)
}




async function createAssignment() {
    const title = document.getElementById("input-title").value;
    const deadline = document.getElementById("input-deadline").value;
    const course_name = document.getElementById("input-course-name").value

    if (!title || !deadline) {
        alert("กรอกข้อมูลให้ครบ");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/assignments/create", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                course_name: course_name,
                title: title,
                deadline: deadline,
                description: ""
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "error");
        }

        uploadAssignmentFile(data.data)
        
        alert("สร้างงานเรียบร้อย!");
    } catch (err) {
        console.error(err);
        alert("สร้างไม่สำเร็จ");
    }
}