function confirmDeleteLesson(lessonId, lessonTitle) {
    if (confirm(`Bạn có chắc chắn muốn xóa bài học "${lessonTitle}"? Hành động này không thể hoàn tác.`)) {
        const form = document.getElementById('delete-lesson-form');
        const baseUrl = form.dataset.deleteUrl;
        form.action = `${baseUrl}${lessonId}/`;
        form.submit();
    }
}

// Sắp xếp bài học bằng kéo thả
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('lessons-container');
    if (container) {
        // Thêm chức năng kéo thả sau khi có Sortable.js
        // Sẽ được thêm trong tương lai khi chúng ta thêm thư viện Sortable.js
        console.log('Lesson container initialized');
    }
});