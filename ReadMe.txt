// 员工姓名，所属部门，权限，线索总量，跟进数量，回退公海数量，成交数量，首单成交总额，成交总额。
// 2025.02.17 完善员工add modal 和update modal
2025.02.18 员工的删除和更新
线索：领取，分配，移交，退回线索池，退回公海，点击打开modal后填写：跟进，退回线索池（限定时间），退回公海
把null 更改为显示为空字符串-

日志：2025.02.20
    tabler.min.css文件中修改了如下css样式
    @media (min-width:1400px){.container,.container-lg,.container-md,.container-sm,.container-xl,.container-xxl{max-width:1600px}}
    /*修改点：max-width:1320px修改成了1600px*/，这里可以控制右侧内容区的显示宽度
    --tblr-bg-surface:#03498c  修改侧栏背景色

日志：2025.02.21
    员工增加了修改功能，再增加个密码修改功能，密码的modal弄好了，做一下views，urls，ajax

日志：2025.02.22
    登录权限制作，认领功能制作中。。。

日志：2025.02.23
    tabler.min.css文件中修改了如下，这个是canvas面板点击显示的宽度
    --tblr-offcanvas-width:400px => --tblr-offcanvas-width:800px

from login.views import required_privilege
@required_privilege('super_admin', 'admin', 'user')