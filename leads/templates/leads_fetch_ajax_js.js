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
                    row.innerHTML = `
                        <td><input class="form-check-input m-0 align-middle" type="checkbox" aria-label="Select invoice" value="${result.lead_id}"></td>
                        <td>${result.contact_person}</td>
                        <td>${result.contact_phone}</td>
                        <td>${result.product_name}</td>
                        <td>${result.business_name}</td>
                        <td>${result.lead_creation_time}</td>
                        <td>${result.department_name}</td>
                        <td>${result.channel_name}</td>
                        <td>${result.component_name}</td>
                        <td>${result.consultation_content}</td>
                        <td>
                            <a class="copy-info" href="#" data-copy-info="
客户姓名：${result.contact_person}
客户电话：${result.contact_phone}
备注：${result.consultation_content_complete}
业务类型：${result.business_name}
线索来源：${result.channel_name}
咨询组件：${result.component_name}
线索领取链接：
${result.absolute_url}{% url 'leads:detail' %}?code=${result.lead_code}
                            ">
                                <i class="fa-solid fa-share-from-square"></i>
                            </a>
                        </td>
                        <td>
                            <a href="#" data-bs-toggle="modal" data-bs-target="#modal-update-app">
                                <i class="fa-solid fa-pen-to-square"></i>
                            </a>
                        </td>
                        <td>
                            <a href="#" data-copy-info="1" onclick=deleteAppData(${result.lead_id})>
                                <i class="fa-solid fa-trash" style="color: red;"></i>
                            </a>
                        </td>
                    `;
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

    // 复制客户信息的点击事件监测函数
    document.addEventListener('DOMContentLoaded', function () {
        // 使用事件委托处理复制操作
        document.addEventListener('click', async function (event) {
            const copyLink = event.target.closest('.copy-info');
            if (copyLink) {
                event.preventDefault();
                const textToCopy = copyLink.getAttribute('data-copy-info').trim();

                try {
                    if ('clipboard' in navigator) {
                        await navigator.clipboard.writeText(textToCopy);
                        showAlert('success');
                    } else {
                        // 传统复制方法
                        const textarea = document.createElement('textarea');
                        textarea.value = textToCopy;
                        document.body.appendChild(textarea);
                        textarea.select();
                        const successful = document.execCommand('copy');
                        document.body.removeChild(textarea);
                        if (successful) {
                            showAlert('success');
                        } else {
                            throw new Error('传统复制方法失败');
                        }
                    }
                } catch (err) {
                    console.error('复制失败: ', err);
                    showAlert('warning');
                }
            }
        });

        function showAlert(type) {
            let alertHtml;
            if (type === 'success') {
                alertHtml = '<div class="alert alert-success" role="alert">信息复制成功，去粘贴吧！</div>';
            } else {
                alertHtml = '<div class="alert alert-warning" role="alert">复制失败，请检查代码！</div>';
            }
            const alertElement = document.createElement('div');
            alertElement.innerHTML = alertHtml;
            document.body.appendChild(alertElement.firstChild);
            setTimeout(() => {
                const alertToRemove = document.querySelector(`.alert-${type}`);
                if (alertToRemove) {
                    alertToRemove.remove();
                }
            }, 1500);
        }
    });

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
