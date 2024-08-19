

class iframeSwitcher{
    constructor(){
        this.buttons = document.querySelectorAll('button');
        this.iframe = document.getElementById('DashBoard_Iframe');
        this.buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.iframe.src = this.urlSwitcher(e.target.id);
            });
        });
    }

    urlSwitcher(buttonID){
        switch (buttonID) {
            case "tasks-due-btn":
                return "tasks-due-report";
            case "tasks-priority-btn":
                return "tasks_priority_due_pie_chart";
            case "urgent-tasks-due-btn":
                return "tasks-urgent-report";
            case "all-tasks-btn":
                return "all_tasks_report";
            default:
                return "tasks-due-report";
        }
    }
}
