async function uploadSubmissionFile(){
    const assignmentId = "1"
    const courseId = "1"

    const dict = {
        "assignment_id":assignmentId,
        "course_id":courseId
    }

    uploadFile('student-file', 'student', "/submission", dict)
}