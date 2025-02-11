/**
 * Quản lý các chức năng trên trang cài đặt
 */
class SettingsManager {
    constructor() {
        this.init();
    }

    /**
     * Khởi tạo các event listeners và trạng thái ban đầu
     */
    init() {
        this.setupTabNavigation();
        this.setupAvatarPreview();
        this.setupFormValidation();
        this.setupNotificationToggles();
        this.restoreActiveTab();
    }

    /**
     * Thiết lập điều hướng tab
     */
    setupTabNavigation() {
        document.querySelectorAll('.settings-nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchTab(item.dataset.target);
            });
        });
    }

    /**
     * Chuyển đổi giữa các tab
     * @param {string} tabId - ID của tab cần hiển thị
     */
    switchTab(tabId) {
        // Cập nhật trạng thái active của navigation items
        document.querySelectorAll('.settings-nav-item').forEach(item => {
            if (item.dataset.target === tabId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Hiển thị panel tương ứng
        document.querySelectorAll('.settings-panel').forEach(panel => {
            if (panel.id === tabId) {
                panel.classList.add('active');
            } else {
                panel.classList.remove('active');
            }
        });

        // Lưu tab đang active vào localStorage
        localStorage.setItem('activeSettingsTab', tabId);

        // Cập nhật URL hash
        window.location.hash = tabId;
    }

    /**
     * Khôi phục tab active từ localStorage hoặc URL hash
     */
    restoreActiveTab() {
        const hash = window.location.hash.slice(1);
        const savedTab = localStorage.getItem('activeSettingsTab');
        const tabToActivate = hash || savedTab || 'profile';
        this.switchTab(tabToActivate);
    }

    /**
     * Thiết lập xem trước ảnh đại diện
     */
    setupAvatarPreview() {
        const avatarInput = document.getElementById('avatar-input');
        if (avatarInput) {
            avatarInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        document.getElementById('avatar-preview').src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                }
            });
        }
    }

    /**
     * Thiết lập validation cho các form
     */
    setupFormValidation() {
        const passwordForm = document.getElementById('password-form');
        if (passwordForm) {
            passwordForm.addEventListener('submit', (e) => {
                const newPass = document.getElementById('new_password').value;
                const confirmPass = document.getElementById('confirm_password').value;
                
                if (newPass !== confirmPass) {
                    e.preventDefault();
                    this.showError('Mật khẩu xác nhận không khớp');
                }
            });
        }
    }

    /**
     * Thiết lập lưu tự động cho các toggle notification
     */
    setupNotificationToggles() {
        document.querySelectorAll('.switch input[type="checkbox"]').forEach(toggle => {
            toggle.addEventListener('change', (e) => {
                const setting = e.target.name;
                const value = e.target.checked;

                // Gửi AJAX request để lưu cài đặt
                fetch('/api/users/settings/notifications/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        setting: setting,
                        value: value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.showSuccess('Đã lưu cài đặt');
                    } else {
                        this.showError('Không thể lưu cài đặt');
                        e.target.checked = !value; // Revert toggle if failed
                    }
                })
                .catch(() => {
                    this.showError('Đã xảy ra lỗi');
                    e.target.checked = !value; // Revert toggle if failed
                });
            });
        });
    }

    /**
     * Hiển thị thông báo lỗi
     * @param {string} message - Nội dung thông báo
     */
    showError(message) {
        this.showNotification(message, 'error');
    }

    /**
     * Hiển thị thông báo thành công
     * @param {string} message - Nội dung thông báo
     */
    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    /**
     * Hiển thị thông báo
     * @param {string} message - Nội dung thông báo
     * @param {string} type - Loại thông báo ('success' hoặc 'error')
     */
    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg text-white ${
            type === 'success' ? 'bg-green-500' : 'bg-red-500'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    /**
     * Lấy CSRF token từ cookie
     * @returns {string} CSRF token
     */
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

/**
 * Hiển thị modal xác nhận xóa tài khoản
 */
function confirmDeleteAccount() {
    const modal = document.getElementById('delete-account-modal');
    modal.classList.remove('hidden');
    modal.classList.add('modal-overlay', 'active');
}

/**
 * Đóng modal xác nhận xóa tài khoản
 */
function closeDeleteModal() {
    const modal = document.getElementById('delete-account-modal');
    modal.classList.remove('active');
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300);
}

// Khởi tạo quản lý cài đặt khi trang đã tải xong
document.addEventListener('DOMContentLoaded', () => {
    window.settingsManager = new SettingsManager();
});