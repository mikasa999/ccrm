<script>


/*
说明：要替换的内容：
appName 替换为app命名空间名称
AppName 替换为app名称，首字母大写
*/


    // 异步加载数据库数据
    function loadAppData() {
        fetch('{% url "cow:get_data" %}')
           .then(response => response.json())
           .then(data => {
                const tableBody = document.getElementById('app-table-body');
                tableBody.innerHTML = ''; // 清空表格内容
                data.results.forEach(result => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><input class="form-check-input m-0 align-middle" type="checkbox" aria-label="Select invoice"></td>
                        <td>${result.cow_employee_name}</td>
                        <td>${result.username}</td>
                        <td>${result.cow_department}</td>
                        <td>${result.cow_privileges}</td>
                        <td>${result.cow_email}</td>
                        <td>${result.cow_leads_total}</td>
                        <td>${result.cow_follow_up_count}</td>
                        <td>${result.cow_customer_count}</td>
                        <td>${result.cow_returned_to_public_count}</td>
                        <td>${result.cow_deal_count}</td>
                        <td>${result.cow_first_deal_total_amount}</td>
                        <td>${result.cow_total_deal_amount}</td>
                        <td><a href="#" data-bs-toggle="modal" data-bs-target="#modal-password-update-app" onclick="preparePasswordUpdateModal(${result.cow_id}, '${result.cow_employee_name}')"><i class="ti ti-fingerprint"></i></a></td>
                        <td><a href="#" data-bs-toggle="modal" data-bs-target="#modal-update-app" onclick="prepareUpdateModal(${result.cow_id}, '${result.cow_employee_name}', '${result.cow_email}', '${result.cow_department}', '${result.cow_privileges}')"><i class="ti ti-edit"></i></a></td>
                        <td><a href="#" onclick="deleteAppData(${result.cow_id})"><i style="color:red;" class="ti ti-archive"></i></a></td>
                    `;
                    tableBody.appendChild(row);
                });
            })
           .catch(error => console.error('Error:', error));
    }

    // 页面加载完成后执行异步加载
    window.addEventListener('load', loadAppData);


    // 准备修改【普通信息】更新模态框里面的数据
    function prepareUpdateModal(arg_cow_id, arg_cow_employee_name, arg_cow_email, arg_cow_department, arg_cow_privileges) {
        const modal = document.getElementById('modal-update-app');
        const cow_id = modal.querySelector('#update-cow-id');
        const cow_employee_name = modal.querySelector('#update-cow-employee-name');
        const cow_email = modal.querySelector('#update-cow-email');
        const cow_department = modal.querySelector('#update-cow-department');
        const cow_privileges = modal.querySelector('#update-cow-privileges');

        cow_id.value = arg_cow_id;
        cow_employee_name.value = arg_cow_employee_name;
        cow_email.value = arg_cow_email;
        cow_department.value = arg_cow_department;
        cow_privileges.value = arg_cow_privileges;
    }

    // 准备修改【密码】更新模态框里面的数据
    function preparePasswordUpdateModal(arg_cow_id, arg_cow_employee_name) {
        const modal = document.getElementById('modal-password-update-app');
        const cow_id = modal.querySelector('#update-password-cow-id');
        const cow_employee_name = modal.querySelector('#update-password-cow-employee-name');

        cow_id.value = arg_cow_id;
        cow_employee_name.value = arg_cow_employee_name;
    }


    // 添加部门
    function addAppData() {
        const cow_employee_name = document.getElementById('add-cow-employee-name').value;
        const cow_email = document.getElementById('add-cow-email').value;
        const cow_department = document.getElementById('add-cow-department').value;
        const cow_privileges = document.getElementById('add-cow-privileges').value;
        const cow_username = document.getElementById('add-cow-username').value;
        const cow_password = document.getElementById('add-cow-password').value;
        const cow_repeat_password = document.getElementById('add-cow-repeat-password').value;

        // 验证密码是否一致
        if (cow_password !== cow_repeat_password) {
            alert('两次输入的密码不一致，请重新填写！');
            return;
        }

        fetch('{% url "cow:add_data" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'cow_employee_name': cow_employee_name,
                'cow_email': cow_email,
                'cow_department': cow_department,
                'cow_privileges': cow_privileges,
                'username': cow_username,
                'password': cow_password,
            })
        })

        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 关闭模态框
                //const modal = document.getElementById('modal-add-app');
                //const modalInstance = bootstrap.Modal.getInstance(modal);
                //modalInstance.hide();
                // 刷新部门数据
                loadAppData();
            } else {
                alert('添加失败：' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }


    // 删除部门
    function deleteAppData(cow_id) {
        if (confirm('确定要删除该部门吗？')) {
            fetch(`{% url "cow:delete_data" 0 %}`.replace('0', cow_id), {
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


    // 修改员工普通信息
    function updateAppData() {
        const cow_id = document.getElementById('update-cow-id').value;
        const cow_employee_name = document.getElementById('update-cow-employee-name').value;
        const cow_email = document.getElementById('update-cow-email').value;
        const cow_department = document.getElementById('update-cow-department').value;
        const cow_privileges = document.getElementById('update-cow-privileges').value;

        fetch(`{% url "cow:update_data" 0 %}`.replace('0', cow_id), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'cow_employee_name': cow_employee_name,
                'cow_email': cow_email,
                'cow_department': cow_department,
                'cow_privileges': cow_privileges,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 刷新部门数据
                loadAppData();
            } else {
                alert('修改失败：' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }


    // 修改员工密码信息
    function updatePasswordAppData() {
        const cow_id = document.getElementById('update-password-cow-id').value;
        const cow_password = document.getElementById('update-password-cow').value;
        const cow_repeat_password = document.getElementById('update-repeat-password-cow').value;

        // 验证密码是否一致
        if (cow_password !== cow_repeat_password) {
            alert('两次输入的密码不一致，请重新填写！');
            return;
        }

        fetch(`{% url "cow:update_password_data" 0 %}`.replace('0', cow_id), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'cow_id': cow_id,
                'password': cow_password,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 刷新部门数据
                loadAppData();
                alert('修改密码成功，可以截图或者拍照记住你修改的密码为：' + cow_password)
            } else {
                alert('修改失败：' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
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
</script>
