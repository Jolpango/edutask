describe('toggle todos', () => {
    let uid;
    let name;
    let email;
  
    let taskUid;
    let taskTitle;
    let taskDesc;
    let taskStart;
    let taskDue;
    let taskUrl;
  
    beforeEach(function () {
      cy.fixture("user.json")
        .then((user) => {
          cy.request({
            method: "POST",
            url: "http://localhost:5000/users/create",
            form: true,
            body: user
          }).then((response) => {
            uid = response.body._id.$oid;
            name = user.firstName + " " + user.lastName;
            email = user.email;
          })
        })
    })
  
    beforeEach(function () {
      cy.fixture("task.json")
        .then((task) => {
          task.userid = uid;
          cy.request({
            method: "POST",
            url: "http://localhost:5000/tasks/create",
            form: true,
            body: task
          }).then((response) => {
            taskUid = response.body._id;
            taskTitle = task.title;
            taskDesc = task.description;
            taskStart = task.start;
            taskDue = task.due;
            taskUrl = task.url;
          })
        })
    })
  
    beforeEach("login", () => {
        cy.visit('http://localhost:3000');
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)
        cy.get("form")
            .submit()
            .then(() => cy.wait(1000));
        cy.get("img")
            .click();
    })

    it("set todo from active to done",() => {    
        // You need double click first time when entering popup 
        cy.get(".checker")
            .click();
        cy.get(".checker")
            .click();
        cy.get(".todo-item")
            .find(".editable")
            .invoke("css", "text-decoration")
            .should("include", "line-through");
    })

    it("set todo from done to active",() => {
        // You need double click first time when entering popup 
        cy.get(".checker")
            .click();
        cy.get(".checker")
            .click();
        cy.get(".todo-item")
            .find(".editable")
            .invoke("css", "text-decoration")
            .should("include", "line-through");
        cy.get(".checker")
            .click();
        cy.get(".todo-item")
            .find(".editable")
            .invoke("css", "text-decoration")
            .should("include", "none");
    })

    afterEach(function () {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
    })
  })
  