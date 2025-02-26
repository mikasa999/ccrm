<script>

    // 异步加载数据库数据
    function loadAppData(page = 1) {
        let url;
        const leads_search_content = document.getElementById('leads_search_content').value;
        if (leads_search_content != '') {
            url = `{% url 'leads:claim_get_data_search' leads_search_content='PLACEHOLDER' %}`.replace('PLACEHOLDER', leads_search_content);
        } else {
            // 不传递参数，使用不带参数的 URL 模式
            url = "{% url 'leads:claim_get_data' %}";
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
                        <td onclick="canvasLeadsData(${result.lead_id});canvasProceedingData(${result.lead_id});" data-bs-toggle="offcanvas" href="#offcanvasEnd" role="button" aria-controls="offcanvasEnd">${result.contact_person}</td>
                        <td>${result.contact_phone}</td>
                        <td>${result.product_name}</td>
                        <td>${result.business_name}</td>
                        <td>${result.lead_creation_time}</td>
                        <td>${result.lead_allocation_time}</td>
                        <td>${result.department_name}</td>
                        <td>${result.channel_name}</td>
                        <td>${result.component_name}</td>
                        <td>${result.consultation_content}</td>
                        <td>${result.cow_name}</td>
                        <td>${result.proceeding_name}</td>
                        <td>${result.follow_new_record}</td>
                        <td>${result.follow_new_time}</td>
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


    // 退回线索池按钮点击事件函数
    function sendBackLeads() {
        //获取 id="app-table-body" 的 tbody 中所有勾选的复选框
        const checkboxes = document.querySelectorAll('#app-table-body input[type="checkbox"]:checked');
        const leadIds = [];
        checkboxes.forEach(checkbox => {
            leadIds.push(checkbox.value);
        });

        if (leadIds.length === 0) {
            alert('请至少选择一条线索退回。');
            return;
        }

        // 使用 fetch API 发送 POST 请求到后端
        fetch('{% url "leads:send_back_leads" %}', {
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
                alert('退回线索池成功。');
                // 刷新部门数据
                loadAppData();
            } else {
                alert('退回线索池失败：' + data.message);
            }
        })
        .catch(error => {
            alert('请求出错：' + error.message);
        });
    }


    // 侧面板异步加载线索详情
    function canvasLeadsData(lead_id) {
        fetch(`{% url "leads:canvas_leads_data" 0 %}`.replace('0', lead_id))
           .then(response => response.json())
           .then(data => {
                const container = document.getElementById('canvas-leads-data');
                container.innerHTML = ''; // 清空容器内容
                data.results.forEach(result => {
                    const div = document.createElement('div');
                    div.className = 'col-xl markdown';
                    div.innerHTML = `
                        <h3>姓名：${result.contact_person}</h3>
                        <strong>电话：${result.contact_phone}</strong><br>
                        业务：${result.business_name} <br>
                        线索创建时间：${result.lead_creation_time}<br>
                        线索领取时间：${result.lead_allocation_time}<br>
                        线索负责人：${result.cow_name}<br>
                        跟进状态：${result.proceeding_name}<br>
                        备注：${result.consultation_content}<br>
                        <div data-lead-id="${lead_id}" style="display:none;"></div>
                        <div data-user-id="${result.username}" style="display:none;"></div>
                    `;
                    container.appendChild(div);
                });
            })
           .catch(error => console.error('Error:', error));
    }


    //侧面板异步加载跟进列表
    function canvasProceedingData(lead_id){
        fetch(`{% url "leads:canvas_proceeding_data" 0 %}`.replace('0', lead_id))
           .then(response => response.json())
           .then(data => {
                const tableBody = document.getElementById('canvas-proceeding-data');
                tableBody.innerHTML = ''; // 清空表格内容
                data.results.forEach(result => {
                    const div = document.createElement('li');
                    div.className = 'step-item active';
                    div.innerHTML = `
                        <div class="h4 m-0">${result.follow_up_time}[${result.follow_up_person}]</div>
                        <div class="text-secondary">${result.follow_up_content}</div>
                    `;
                    tableBody.appendChild(div);
                });
            })
           .catch(error => console.error('Error:', error));
    }


    //侧面板表单提交，跟进状态 + 添加跟进 分别添加到不同的数据表中
    function canvasProceedingAdd() {
        // 提前声明变量，扩大作用域
        let leadId;
        let userId;

        // 使用 querySelector 选择具有 data-lead-id 属性的元素
        const element = document.querySelector('[data-lead-id]');
        if (element) {
            // 使用 dataset 获取 data-lead-id 的值
            leadId = element.dataset.leadId;
        } else {
            alert('没有获取到该id值');
            return; // 如果未获取到 leadId，直接返回，避免后续错误
        }

        // 使用 querySelector 选择具有 data-user-id 属性的元素
        const element_user_id = document.querySelector('[data-user-id]');
        if (element_user_id) {
            // 使用 dataset 获取 data-user-id 的值
            userId = element_user_id.dataset.userId;
        } else {
            alert('没有获取到该id值');
            return; // 如果未获取到 userId，直接返回，避免后续错误
        }

        const lead_id = Number(leadId);
        const follow_up_person = userId;
        const follow_up_content = document.getElementById('follow_up_content').value;
        const proceeding_name = document.getElementById('canvas-proceeding-select').value;

        //判断一下select提交的跟进状态
        if (proceeding_name=='proceeding-error'){
            alert('请先选择跟进状态！');
            return;
        }
        //判断一下提交过来的跟进内容是否为空
        if (follow_up_content==''){
            alert('请填写跟进内容！');
            return;
        }

        fetch('{% url "leads:canvas_proceeding_add" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'lead_id': lead_id,
                'follow_up_person': follow_up_person,
                'follow_up_content': follow_up_content,
                'proceeding_name': proceeding_name,
            })
        })
       .then(response => response.json())
       .then(data => {
            if (data.status === 'success') {
                // 刷新部门数据
                alert(data.message);
                loadAppData();
                canvasLeadsData(leadId);
                canvasProceedingData(leadId);
            } else {
                alert('添加失败：' + data.message);
            }
        })
       .catch(error => console.error('Error:', error));
    }

</script>
