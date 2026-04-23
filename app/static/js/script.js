/**
 * KPI Pro - Data Sync System
 * Main JavaScript file for UI interactivity
 */

// ==================== Sync Functionality ====================

/**
 * Trigger the data synchronization process
 */
async function triggerSync() {
    const syncBtn = document.getElementById('sync-btn');
    const resetBtn = document.getElementById('reset-btn');
    const statusMsg = document.getElementById('status-message');
    const spinner = document.getElementById('loading-spinner');
    const resultSection = document.getElementById('result-section');
    const lastStatus = document.getElementById('last-status');

    // Disable button and show loading spinner
    syncBtn.disabled = true;
    spinner.style.display = 'block';
    statusMsg.style.display = 'none';
    resultSection.style.display = 'none';

    // Update status
    lastStatus.textContent = 'Syncing...';
    lastStatus.className = 'value status-loading';

    try {
        // Send sync request to backend
        const response = await fetch('/sync', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            // Success
            showSuccessMessage(`✓ Sync completed successfully! ${data.rows} rows synced.`, data.rows);
            lastStatus.textContent = 'Success';
            lastStatus.className = 'value status-success';
            logActivity(`✓ Data sync completed: ${data.rows} rows synchronized`);
        } else {
            // Error from backend
            showErrorMessage(`✗ Sync failed: ${data.error || 'Unknown error'}`);
            lastStatus.textContent = 'Failed';
            lastStatus.className = 'value status-error';
            logActivity(`✗ Sync failed: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        // Network or other error
        showErrorMessage(`✗ Error connecting to server: ${error.message}`);
        lastStatus.textContent = 'Error';
        lastStatus.className = 'value status-error';
        logActivity(`✗ Connection error: ${error.message}`);
        console.error('Sync error:', error);
    } finally {
        // Re-enable button and hide spinner
        syncBtn.disabled = false;
        spinner.style.display = 'none';
        resetBtn.style.display = 'inline-flex';
    }
}

/**
 * Show success message in the UI
 */
function showSuccessMessage(message, rowCount) {
    const statusMsg = document.getElementById('status-message');
    const resultSection = document.getElementById('result-section');
    const rowCount_el = document.getElementById('row-count');
    const syncTime = document.getElementById('sync-timestamp');

    statusMsg.textContent = message;
    statusMsg.className = 'status-message success';
    statusMsg.style.display = 'block';

    // Show result section
    rowCount_el.textContent = rowCount;
    syncTime.textContent = new Date().toLocaleString();
    resultSection.style.display = 'block';
}

/**
 * Show error message in the UI
 */
function showErrorMessage(message) {
    const statusMsg = document.getElementById('status-message');
    statusMsg.textContent = message;
    statusMsg.className = 'status-message error';
    statusMsg.style.display = 'block';
}

/**
 * Reset the sync status
 */
function resetStatus() {
    const syncBtn = document.getElementById('sync-btn');
    const resetBtn = document.getElementById('reset-btn');
    const statusMsg = document.getElementById('status-message');
    const resultSection = document.getElementById('result-section');
    const lastStatus = document.getElementById('last-status');

    statusMsg.style.display = 'none';
    resultSection.style.display = 'none';
    lastStatus.textContent = 'Ready';
    lastStatus.className = 'value status-idle';
    syncBtn.style.display = 'inline-flex';
    resetBtn.style.display = 'none';
}

/**
 * Trigger monthly KPI report synchronization with year
 */
async function triggerMonthlySyncWithYear() {
    const yearInput = document.getElementById('year-input');
    const year = parseInt(yearInput.value) || 2026;
    
    const syncBtn = document.getElementById('monthly-sync-btn');
    const resetBtn = document.getElementById('monthly-reset-btn');
    const statusMsg = document.getElementById('monthly-status-message');
    const spinner = document.getElementById('monthly-loading-spinner');
    const resultSection = document.getElementById('monthly-result-section');
    const lastStatus = document.getElementById('monthly-sync-status');

    // Validate year
    if (year < 2018 || year > 2099) {
        showMonthlySyncErrorMessage('Invalid year. Please enter a year between 2018 and 2099.');
        return;
    }

    // Disable button and show loading spinner
    syncBtn.disabled = true;
    spinner.style.display = 'block';
    statusMsg.style.display = 'none';
    resultSection.style.display = 'none';

    // Update status
    lastStatus.textContent = 'Syncing...';
    lastStatus.className = 'value status-loading';

    try {
        // Send monthly sync request to backend with year
        const response = await fetch('/api/sync/monthly-kpi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ year: year })
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            // Success
            showMonthlySyncSuccessMessage(
                `✓ Monthly KPI sync completed successfully! ${data.rows} rows synced for year ${year}.`,
                data.rows,
                year
            );
            lastStatus.textContent = 'Success';
            lastStatus.className = 'value status-success';
            logActivity(`✓ Monthly KPI sync completed for year ${year}: ${data.rows} rows synchronized`);
        } else {
            // Error from backend
            showMonthlySyncErrorMessage(`✗ Sync failed: ${data.error || 'Unknown error'}`);
            lastStatus.textContent = 'Failed';
            lastStatus.className = 'value status-error';
            logActivity(`✗ Monthly KPI sync failed for year ${year}: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        // Network or other error
        showMonthlySyncErrorMessage(`✗ Error connecting to server: ${error.message}`);
        lastStatus.textContent = 'Error';
        lastStatus.className = 'value status-error';
        logActivity(`✗ Monthly KPI sync connection error: ${error.message}`);
        console.error('Monthly sync error:', error);
    } finally {
        // Re-enable button and hide spinner
        syncBtn.disabled = false;
        spinner.style.display = 'none';
        resetBtn.style.display = 'inline-flex';
    }
}

/**
 * Show success message for monthly sync
 */
function showMonthlySyncSuccessMessage(message, rowCount, year) {
    const statusMsg = document.getElementById('monthly-status-message');
    const resultSection = document.getElementById('monthly-result-section');
    const rowCountEl = document.getElementById('monthly-row-count');
    const yearEl = document.getElementById('monthly-sync-year');
    const syncTime = document.getElementById('monthly-sync-timestamp');

    statusMsg.textContent = message;
    statusMsg.className = 'status-message success';
    statusMsg.style.display = 'block';

    // Show result section
    yearEl.textContent = year;
    rowCountEl.textContent = rowCount;
    syncTime.textContent = new Date().toLocaleString();
    resultSection.style.display = 'block';
}

/**
 * Show error message for monthly sync
 */
function showMonthlySyncErrorMessage(message) {
    const statusMsg = document.getElementById('monthly-status-message');
    statusMsg.textContent = message;
    statusMsg.className = 'status-message error';
    statusMsg.style.display = 'block';
}

/**
 * Reset the monthly sync status
 */
function resetMonthlySyncStatus() {
    const syncBtn = document.getElementById('monthly-sync-btn');
    const resetBtn = document.getElementById('monthly-reset-btn');
    const statusMsg = document.getElementById('monthly-status-message');
    const resultSection = document.getElementById('monthly-result-section');
    const lastStatus = document.getElementById('monthly-sync-status');

    statusMsg.style.display = 'none';
    resultSection.style.display = 'none';
    lastStatus.textContent = 'Ready';
    lastStatus.className = 'value status-idle';
    syncBtn.style.display = 'inline-flex';
    resetBtn.style.display = 'none';
}

// ==================== Activity Logging ====================

/**
 * Log an activity to the activity log
 */
function logActivity(message) {
    const logContainer = document.getElementById('sync-log');
    if (!logContainer) return;

    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';

    const timestamp = new Date().toLocaleTimeString();
    logEntry.innerHTML = `
        <span class="log-time">${timestamp}</span>
        <span class="log-message">${escapeHtml(message)}</span>
    `;

    logContainer.insertBefore(logEntry, logContainer.firstChild);

    // Keep only the last 50 entries
    while (logContainer.children.length > 50) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ==================== Search and Filter ====================

/**
 * Setup search functionality
 */
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;

    searchInput.addEventListener('input', function () {
        filterTable();
    });
}

/**
 * Setup filter functionality
 */
function setupFilter() {
    const filterDept = document.getElementById('filter-department');
    if (!filterDept) return;

    filterDept.addEventListener('change', function () {
        filterTable();
    });
}

/**
 * Filter the data table
 */
function filterTable() {
    const searchInput = document.getElementById('search-input');
    const filterDept = document.getElementById('filter-department');
    const tbody = document.getElementById('data-tbody');

    if (!tbody) return;

    const searchValue = (searchInput?.value || '').toLowerCase();
    const filterValue = (filterDept?.value || '').toLowerCase();

    const rows = tbody.querySelectorAll('tr:not(.empty-row)');

    let visibleCount = 0;
    rows.forEach(row => {
        let shouldShow = true;

        // Check search filter
        if (searchValue) {
            const rowText = row.textContent.toLowerCase();
            shouldShow = rowText.includes(searchValue);
        }

        // Check department filter
        if (shouldShow && filterValue) {
            const deptCell = row.cells[5]; // Department is in 6th column
            shouldShow = deptCell && deptCell.textContent.toLowerCase().includes(filterValue);
        }

        row.style.display = shouldShow ? '' : 'none';
        if (shouldShow) visibleCount++;
    });

    // Show empty message if no results
    if (visibleCount === 0) {
        const emptyRow = tbody.querySelector('.empty-row');
        if (emptyRow) emptyRow.style.display = '';
    }
}

// ==================== Pagination ====================

/**
 * Setup pagination
 */
let currentPageNum = 1;
const itemsPerPage = 10;

function setupPagination() {
    const prevBtn = document.querySelector('.table-pagination button:first-child');
    const nextBtn = document.querySelector('.table-pagination button:last-child');

    if (prevBtn) {
        prevBtn.addEventListener('click', previousPage);
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', nextPage);
    }
}

function previousPage() {
    if (currentPageNum > 1) {
        currentPageNum--;
        updatePagination();
    }
}

function nextPage() {
    const tbody = document.getElementById('data-tbody');
    if (!tbody) return;

    const totalRows = tbody.querySelectorAll('tr:not(.empty-row)').length;
    const totalPages = Math.ceil(totalRows / itemsPerPage);

    if (currentPageNum < totalPages) {
        currentPageNum++;
        updatePagination();
    }
}

function updatePagination() {
    const tbody = document.getElementById('data-tbody');
    const pageInfo = document.getElementById('current-page');

    if (!tbody) return;

    const rows = tbody.querySelectorAll('tr:not(.empty-row)');
    const start = (currentPageNum - 1) * itemsPerPage;
    const end = start + itemsPerPage;

    rows.forEach((row, index) => {
        row.style.display = (index >= start && index < end) ? '' : 'none';
    });

    if (pageInfo) {
        pageInfo.textContent = `Page ${currentPageNum}`;
    }
}

// ==================== Keyboard Shortcuts ====================

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function (e) {
        // Ctrl/Cmd + S to sync
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const syncBtn = document.getElementById('sync-btn');
            if (syncBtn && !syncBtn.disabled) {
                triggerSync();
            }
        }

        // Ctrl/Cmd + R to reset (but not the browser reload)
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            const resetBtn = document.getElementById('reset-btn');
            if (resetBtn && resetBtn.style.display !== 'none') {
                e.preventDefault();
                resetStatus();
            }
        }
    });
}

// ==================== Chart Placeholder ====================

/**
 * Initialize empty charts with placeholder
 */
function initCharts() {
    // This is where you would initialize real charts
    // using a library like Chart.js, Plotly, or similar
    console.log('Chart initialization placeholder');
}

// ==================== Page Load ====================

/**
 * Initialize the page when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function () {
    console.log('KPI Pro initialized');

    // Setup all functionality
    setupSearch();
    setupFilter();
    setupPagination();
    setupKeyboardShortcuts();
    initCharts();

    // Log initial activity
    logActivity('✓ System ready for synchronization');

    // Show initial info
    showInfoNotification('Press Ctrl+S to sync data, or click the Start Sync button');
});

/**
 * Show an info notification
 */
function showInfoNotification(message) {
    // You can enhance this with a toast notification system
    console.info(message);
}

// ==================== Export Functions ====================

/**
 * Export table data to CSV
 */
function exportTableToCSV(filename = 'kpi-data.csv') {
    const tbody = document.getElementById('data-tbody');
    if (!tbody) return;

    let csv = 'KPI ID,Name,Year,Month,Value,Department,Status\n';

    const rows = tbody.querySelectorAll('tr:not(.empty-row)');
    rows.forEach(row => {
        const cells = Array.from(row.cells).map(cell => `"${cell.textContent}"`);
        csv += cells.join(',') + '\n';
    });

    downloadCSV(csv, filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
}

// ==================== Error Handler ====================

/**
 * Global error handler
 */
window.addEventListener('error', function (event) {
    console.error('Global error:', event.error);
    logActivity(`⚠️ Error: ${event.error?.message || 'Unknown error'}`);
});

/**
 * Unhandled promise rejection handler
 */
window.addEventListener('unhandledrejection', function (event) {
    console.error('Unhandled promise rejection:', event.reason);
    logActivity(`⚠️ Promise rejection: ${event.reason?.message || 'Unknown error'}`);
});
