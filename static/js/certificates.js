/**
 * Xử lý tải chứng chỉ
 * @param {string} certificateNumber - Mã chứng chỉ
 */
function downloadCertificate(certificateNumber) {
    // Mở trang chứng chỉ trong tab mới để in/tải về
    window.open(`/courses/certificates/${certificateNumber}/`);
}

/**
 * Hiển thị modal chia sẻ chứng chỉ
 * @param {string} certificateNumber - Mã chứng chỉ
 */
function shareCertificate(certificateNumber) {
    const modal = document.getElementById('shareModal');
    const urlInput = document.getElementById('certificateUrl');
    const url = `${window.location.origin}/courses/certificates/${certificateNumber}/`;
    
    urlInput.value = url;
    modal.classList.remove('hidden');
}

/**
 * Sao chép liên kết chia sẻ vào clipboard
 */
function copyShareLink() {
    const urlInput = document.getElementById('certificateUrl');
    urlInput.select();
    document.execCommand('copy');
    
    // Hiển thị thông báo
    const notification = document.createElement('div');
    notification.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg';
    notification.textContent = 'Đã sao chép liên kết!';
    document.body.appendChild(notification);
    
    // Xóa thông báo sau 2 giây
    setTimeout(() => {
        notification.remove();
    }, 2000);
}

/**
 * Đóng modal chia sẻ
 */
function closeShareModal() {
    const modal = document.getElementById('shareModal');
    modal.classList.add('hidden');
}

// Xử lý đóng modal khi click ra ngoài
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('shareModal');
    document.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeShareModal();
        }
    });
});

/**
 * Xác thực chứng chỉ
 * @param {string} certificateNumber - Mã chứng chỉ cần xác thực
 * @returns {Promise} Kết quả xác thực
 */
async function verifyCertificate(certificateNumber) {
    try {
        const response = await fetch(`/courses/certificates/verify/?number=${certificateNumber}`);
        const data = await response.json();
        
        const resultElement = document.getElementById('verificationResult');
        if (data.valid) {
            resultElement.innerHTML = `
                <div class="p-4 bg-green-100 text-green-700 rounded-lg">
                    <h3 class="font-bold mb-2">✓ Chứng chỉ hợp lệ</h3>
                    <p>Cấp cho: ${data.issued_to}</p>
                    <p>Khóa học: ${data.course}</p>
                    <p>Ngày cấp: ${data.issued_date}</p>
                </div>
            `;
        } else {
            resultElement.innerHTML = `
                <div class="p-4 bg-red-100 text-red-700 rounded-lg">
                    <h3 class="font-bold mb-2">✗ Chứng chỉ không hợp lệ</h3>
                    <p>Không tìm thấy thông tin chứng chỉ này trong hệ thống.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error verifying certificate:', error);
        const resultElement = document.getElementById('verificationResult');
        resultElement.innerHTML = `
            <div class="p-4 bg-red-100 text-red-700 rounded-lg">
                <h3 class="font-bold mb-2">✗ Lỗi xác thực</h3>
                <p>Đã có lỗi xảy ra trong quá trình xác thực. Vui lòng thử lại sau.</p>
            </div>
        `;
    }
}