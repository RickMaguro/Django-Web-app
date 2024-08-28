

/**
 * This class handles the switching of iframes based on the button clicked. in the Dashboard.html
 */
class iframeSwitcher{
    /**
     * Constructor for the iframeSwitcher class.
     * It also adds event listeners to the buttons to switch the iframe src when clicked.
     */
    constructor(){
        // Get all the buttons in the document
        this.buttons = document.querySelectorAll('button');
        // Get the iframe element with the id 'DashBoard_Iframe'
        this.iframe = document.getElementById('DashBoard_Iframe');
        
        // Add event listeners to the buttons
        this.buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                // Get the id of the clicked button
                let buttonId = e.target.id;
                // Switch the iframe src based on the button id
                this.iframe.src = this.urlSwitcher(buttonId);
            });
        });
    }

    //This function switches the iframe src based on the button id.
    urlSwitcher(buttonID){
        // Switch statement to determine the url of the iframe based on the button id
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
