/**
 * Xử lý chuyển đổi tab và lọc khóa học
 */
class CourseManager {
    constructor() {
        this.tabButtons = document.querySelectorAll('.tab-button');
        this.courseCards = document.querySelectorAll('.course-card');
        this.init();
    }

    /**
     * Khởi tạo sự kiện cho các tab
     */
    init() {
        this.switchTab('all');
        this.setupTabListeners();
    }

    /**
     * Thiết lập các sự kiện cho tab
     */
    setupTabListeners() {
        this.tabButtons.forEach(tab => {
            tab.addEventListener('click', () => {
                const status = tab.id.replace('tab-', '');
                this.switchTab(status);
            });
        });
    }

    /**
     * Chuyển đổi giữa các tab và lọc khóa học
     * @param {string} status - Trạng thái cần lọc ('all', 'in-progress', 'completed')
     */
    switchTab(status) {
        // Cập nhật trạng thái active của các tab
        this.tabButtons.forEach(tab => {
            if (tab.id === `tab-${status}`) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });

        // Lọc và hiển thị các khóa học
        this.courseCards.forEach(card => {
            if (status === 'all' || card.dataset.status === status) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });

        // Lưu trạng thái tab hiện tại vào localStorage
        localStorage.setItem('selectedCourseTab', status);
    }

    /**
     * Khôi phục tab đã chọn trước đó
     */
    restoreSelectedTab() {
        const selectedTab = localStorage.getItem('selectedCourseTab');
        if (selectedTab) {
            this.switchTab(selectedTab);
        }
    }
}

// Khởi tạo quản lý khóa học khi trang đã tải xong
document.addEventListener('DOMContentLoaded', () => {
    const courseManager = new CourseManager();
    courseManager.restoreSelectedTab();
});