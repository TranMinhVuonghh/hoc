document.addEventListener('DOMContentLoaded', function() {
    // Xử lý xem trước ảnh
    const imageInput = document.querySelector('input[type="file"]');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = document.querySelector('img');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'w-full h-48 object-cover rounded-lg mb-4';
                        imageInput.parentElement.insertBefore(preview, imageInput);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Tự động tạo slug từ tiêu đề
    const titleInput = document.getElementById('title');
    const slugInput = document.getElementById('slug');
    
    if (titleInput && slugInput && window.isNewCourse) {
        titleInput.addEventListener('input', function() {
            const slug = this.value
                .toLowerCase()
                .normalize('NFD')
                .replace(/[-]/g, '')
                .replace(/đ/g, 'd')
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/^-+|-+$/g, '');
            slugInput.value = slug;
        });
    }
});

// Xác nhận xóa khóa học
function confirmDelete() {
    if (confirm('Bạn có chắc chắn muốn xóa khóa học này? Hành động này không thể hoàn tác.')) {
        document.getElementById('delete-course-form').submit();
    }
}