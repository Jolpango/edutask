describe('create todo item', () => {
  let uid;
  let name;
  let email;

  let taskUid;
  let taskTitle;
  let taskDesc;
  let taskStart;
  let taskDue;
  let taskUrl;

  before(function () {
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

  before(function () {
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

  it("check if add is disabled when empty", () => {
    cy.get(".popup")
    .find("input[type='submit']")
    .should("be.disabled");
})

  it("create a new todo item", () => {
      cy.get(".popup")
        .find("input")
        .first()
        .type("hello");
      cy.get(".popup")
        .find("form")
        .submit();
      cy.get(".todo-item")
        .should("contain.text", "hello")
  })

  after(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
