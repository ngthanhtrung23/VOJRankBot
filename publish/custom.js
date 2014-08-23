"use strict";
$(document).ready(function () {
    load_user_rank()
    load_problem_list()

    var current_tab = "user-rank";
    console.log(current_tab);

    $(".toggle").click(function (event) {
        var node = $(event.target);
        var new_id = node.attr("show"), old_tab = current_tab;
        if (new_id === current_tab) {
            return ;
        }
        current_tab = new_id;
        $("#" + old_tab + "-toggle").parent().toggleClass("active");
        $("#" + old_tab).hide(function () {
            $("#" + new_id).show();
            $('#' + new_id + "-toggle").parent().toggleClass("active");
        });
    })
});

function load_user_rank() {
    var html = '', i, user;
    for(i = 0; i < rank_users.length; i += 1) {
        user = rank_users[i];
        html += "<tr>"
                + "<td>" + user[0] + "</td>"
                + "<td><a href='http://vn.spoj.com/users/" + user[1] + "'>" + user[1] + "</a></td>"
                + "<td>" + user[2] + "</td>"
                + "<td>" + user[3] + "</td>"
                + "</tr>";
    }
    $("#user-rank-table").html("");
    $("#user-rank-table").append("<tr>"
                + "<th onclick='sort_user_by_rank()'>#</th>"
                + "<th onclick='sort_user_by_account()'>User</th>"
                + "<th>Organization</th>"
                + "<th onclick='sort_user_by_rank()'>Score</th>"
                + "</tr>");
    $("#user-rank-table").append(html);
}

function load_problem_list() {
    var html = '', i, problem;
    for(i = 0; i < problem_list.length; i += 1) {
        problem = problem_list[i];
        html += "<tr class='" + problem[1] + "'>"
                + "<td>" + problem[0] + "</td>"
                + "<td>" + problem[1] + "</td>"
                + "<td><a href='http://vn.spoj.com/problems/" + problem[2] + "'>" + problem[2] + "</a></td>"
                + "<td>" + problem[3] + "</td>"
                + "<td>" + problem[4] + "</td>"
                + "<td>" + problem[5] + "</td>"
                + "</tr>"
    }
    $("#problem-list-table").html("");
    $("#problem-list-table").append("<tr>"
                + "<th onclick='sort_problem_by_type()'>#</th>"
                + "<th onclick='sort_problem_by_type()'>Type</th>"
                + "<th onclick='sort_problem_by_id()'>ID</th>"
                + "<th>Name</th>"
                + "<th onclick='sort_problem_by_ac()'>Number of AC</th>"
                + "<th onclick='sort_problem_by_score()'>Score</th>"
                + "</tr>");
    $("#problem-list-table").append(html);

    if (!$("#acm-toggle").is(":checked")) {
        $(".acm").hide();
    }
    if (!$("#oi-toggle").is(":checked")) {
        $(".oi").hide();
    }
}

function cmp_user_account(x, y) {
    return (x[1] < y[1]) ? (-1) : ((x[1] > y[1]) ? 1 : 0);
}

function cmp_user_rank(x, y) {
    return x[0] - y[0];
}

function sort_user_by_account() {
    rank_users.sort(cmp_user_account);
    load_user_rank();
}

function sort_user_by_rank() {
    rank_users.sort(cmp_user_rank);
    load_user_rank();
}

function cmp_problem_id(x, y) {
    return (x[2] < y[2]) ? (-1) : ((x[2] > y[2]) ? 1 : 0);
}

function cmp_problem_type(x, y) {
    return x[0] - y[0];
}

function cmp_problem_by_ac(x, y) {
    return x[4] - y[4];
}

function cmp_problem_by_score(x, y) {
    return x[5] - y[5];
}

function sort_problem_by_id() {
    problem_list.sort(cmp_problem_id);
    load_problem_list();
}

function sort_problem_by_type() {
    problem_list.sort(cmp_problem_type);
    load_problem_list();
}

function sort_problem_by_ac() {
    problem_list.sort(cmp_problem_by_ac);
    load_problem_list();
}

function sort_problem_by_score() {
    problem_list.sort(cmp_problem_by_score);
    load_problem_list();
}
