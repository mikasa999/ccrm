<script>

    // 异步加载数据库数据
    function loadAppData(page = 1) {
        let url;
        const leads_search_content = document.getElementById('leads_search_content').value;
        if (leads_search_content != '') {
            url = `{% url 'leads:get_data_search' leads_search_content='PLACEHOLDER' %}`.replace('PLACEHOLDER', leads_search_content);
        } else {
            // 不传递参数，使用不带参数的 URL 模式
            url = "{% url 'leads:get_data' %}";
        }
        // 添加分页参数
        url += `?page=${page}`;

        fetch(url)
          .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
          .then(data => {
                const tableBody = document.getElementById('app-table-body');
                tableBody.innerHTML = ''; // 清空表格内容
                data.results.forEach(result => {
                    const row = document.createElement('tr');
                    const createCell = (text) => {
                        const cell = document.createElement('td');
                        cell.textContent = text;
                        return cell;
                    };

                    const checkboxCell = document.createElement('td');
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.className = 'form-check-input m-0 align-middle';
                    checkbox.ariaLabel = 'Select invoice';
                    checkbox.id = `checkbox-${result.lead_id}`;
                    checkbox.value = result.lead_id;
                    checkboxCell.appendChild(checkbox);
                    row.appendChild(checkboxCell);

                    row.appendChild(createCell(result.contact_person));
                    row.appendChild(createCell(result.contact_phone));
                    row.appendChild(createCell(result.product_name));
                    row.appendChild(createCell(result.business_name));
                    row.appendChild(createCell(result.lead_creation_time));
                    row.appendChild(createCell(result.department_name));
                    row.appendChild(createCell(result.channel_name));
                    row.appendChild(createCell(result.component_name));
                    row.appendChild(createCell(result.consultation_content));

                    const copyCell = document.createElement('td');
                    const copyLink = document.createElement('a');
                    copyLink.href = '#';
                    copyLink.dataset.bsToggle = 'modal';
                    copyLink.dataset.bsTarget = '#modal-update-app';
                    copyLink.onclick = () => prepareUpdateModal(result.lead_id, result.appName_name, result.appName_code);
                    const copyIcon = document.createElement('i');
                    copyIcon.className = 'ti ti-clipboard-copy';
                    copyLink.appendChild(copyIcon);
                    copyCell.appendChild(copyLink);
                    row.appendChild(copyCell);

                    const editCell = document.createElement('td');
                    const editLink = document.createElement('a');
                    editLink.href = '#';
                    editLink.dataset.bsToggle = 'modal';
                    editLink.dataset.bsTarget = '#modal-update-app';
                    editLink.onclick = () => prepareUpdateModal(result.lead_id, result.appName_name, result.appName_code);
                    const editIcon = document.createElement('i');
                    editIcon.className = 'ti ti-edit';
                    editLink.appendChild(editIcon);
                    editCell.appendChild(editLink);
                    row.appendChild(editCell);

                    const deleteCell = document.createElement('td');
                    const deleteLink = document.createElement('a');
                    deleteLink.href = '#';
                    deleteLink.onclick = () => deleteAppData(result.lead_id);
                    const deleteIcon = document.createElement('i');
                    deleteIcon.style.color = 'red';
                    deleteIcon.className = 'ti ti-archive';
                    deleteLink.appendChild(deleteIcon);
                    deleteCell.appendChild(deleteLink);
                    row.appendChild(deleteCell);

                    tableBody.appendChild(row);
                });

                // 更新分页导航栏
                const pagination = document.querySelector('.pagination');
                pagination.innerHTML = '';

                const prevPage = document.createElement('li');
                prevPage.className = 'page-item';
                if (data.current_page === 1) {
                    prevPage.classList.add('disabled');
                }
                const prevLink = document.createElement('a');
                prevLink.className = 'page-link';
                prevLink.href = '#';
                prevLink.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                         stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                         stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M15 6l-6 6l6 6"></path>
                    </svg>
                    上一页
                `;
                prevLink.onclick = () => loadAppData(data.current_page - 1);
                prevPage.appendChild(prevLink);
                pagination.appendChild(prevPage);

                for (let i = 1; i <= data.total_pages; i++) {
                    const pageItem = document.createElement('li');
                    pageItem.className = 'page-item';
                    if (i === data.current_page) {
                        pageItem.classList.add('active');
                    }
                    const pageLink = document.createElement('a');
                    pageLink.className = 'page-link';
                    pageLink.href = '#';
                    pageLink.textContent = i;
                    pageLink.onclick = () => loadAppData(i);
                    pageItem.appendChild(pageLink);
                    pagination.appendChild(pageItem);
                }

                const nextPage = document.createElement('li');
                nextPage.className = 'page-item';
                if (data.current_page === data.total_pages) {
                    nextPage.classList.add('disabled');
                }
                const nextLink = document.createElement('a');
                nextLink.className = 'page-link';
                nextLink.href = '#';
                nextLink.innerHTML = `
                    下一页
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                         stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                         stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M9 6l6 6l-6 6"></path>
                    </svg>
                `;
                nextLink.onclick = () => loadAppData(data.current_page + 1);
                nextPage.appendChild(nextLink);
                pagination.appendChild(nextPage);

                // 更新记录总数
                const recordCount = document.querySelector('.card-footer p');
                recordCount.textContent = `共查询到${data.total_records}条纪录`;
            })
          .catch(error => console.error('Error:', error));
    }


    // 页面加载完成后执行异步加载
    window.addEventListener('load', loadAppData);


    // 添加线索
    function addAppData() {
        const contact_person = document.getElementById('leads-contact-person').value;
        const contact_phone = document.getElementById('leads-contact-phone').value;
        const product_name = document.getElementById('leads-product-name').value;
        const business_name = document.getElementById('leads-business-name').value;
        const department_name = document.getElementById('leads-department-name').value;
        const channel_name = document.getElementById('leads-channel-name').value;
        const component_name = document.getElementById('leads-component-name').value;
        const consultation_content = document.getElementById('leads-consultation-content').value;

        fetch('{% url "leads:add_data" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'contact_person': contact_person,
                'contact_phone': contact_phone,
                'product_name': product_name,
                'business_name': business_name,
                'department_name': department_name,
                'channel_name': channel_name,
                'component_name': component_name,
                'consultation_content': consultation_content,
            })
        })

        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 刷新部门数据
                loadAppData();
            } else {
                alert('添加失败：' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }


    // 删除线索
    function deleteAppData(lead_id) {
        if (confirm('确定要删除该部门吗？')) {
            fetch(`{% url "leads:delete_data" 0 %}`.replace('0', lead_id), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // 刷新部门数据
                    loadAppData();
                } else {
                    alert('删除失败：' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }


    // 获取 CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie!== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    // 认领线索按钮点击事件函数
    function claimLeads() {
        //获取 id="app-table-body" 的 tbody 中所有勾选的复选框
        const checkboxes = document.querySelectorAll('#app-table-body input[type="checkbox"]:checked');
        const leadIds = [];
        checkboxes.forEach(checkbox => {
            leadIds.push(checkbox.value);
        });

        if (leadIds.length === 0) {
            alert('请至少选择一条线索进行认领。');
            return;
        }

        // 使用 fetch API 发送 POST 请求到后端
        fetch('{% url "leads:claim_leads" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}' // 添加 CSRF 令牌
            },
            body: JSON.stringify({
                lead_ids: leadIds
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不正常');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('线索认领成功。');
                // 刷新部门数据
                loadAppData();
            } else {
                alert('线索认领失败：' + data.message);
            }
        })
        .catch(error => {
            alert('请求出错：' + error.message);
        });
    }

</script>
