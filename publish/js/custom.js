"use strict";
$(document).ready(function () {
    load_user_rank()
    load_problem_list()

    var current_tab = "user-rank";

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
                + "<td></td>"
                + "</tr>";
    }
    $("#user-rank-table").html("");
    $("#user-rank-table").append("<tr>"
                + "<th onclick='reload_user(0)'>#&nbsp;<span class='glyphicon glyphicon-sort-by-attributes'></span></th>"
                + "<th onclick='reload_user(1)'>Thành viên&nbsp;<span class='glyphicon glyphicon-sort-by-alphabet'></span></th>"
                + "<th>Trường / đơn vị</th>"
                + "<th onclick='reload_user(0)'>Điểm&nbsp;<span class='glyphicon glyphicon-sort-by-attributes-alt'></span></th>"
                + "<th>Số bài</th>"
                + "</tr>");
    $("#user-rank-table").append(html);
}

function load_problem_list() {
    var html = '', i, problem;
    for(i = 0; i < problem_list.length; i += 1) {
        problem = problem_list[i];
        html += "<tr class='" + problem[1] + "'>"
                + "<td>" + problem[1] + "</td>"
                + "<td><a href='http://vn.spoj.com/problems/" + problem[2] + "'>" + problem[2] + "</a></td>"
                + "<td>" + problem[3] + "</td>"
                + "<td>" + problem[4] + "</td>"
                + "<td>" + problem[5] + "</td>"
                + "</tr>"
    }
    $("#problem-list-table").html("");
    $("#problem-list-table").append("<tr>"
                + "<th onclick='reload_problem(0)'>Loại bài&nbsp;<span class='glyphicon glyphicon-sort-by-alphabet'></span></th>"
                + "<th onclick='reload_problem(2)'>Mã bài&nbsp;<span class='glyphicon glyphicon-sort-by-alphabet'></span></th>"
                + "<th>Tên bài</th>"
                + "<th onclick='reload_problem(4)'>Số người giải được&nbsp;<span class='glyphicon glyphicon-sort-by-attributes'></span></th>"
                + "<th onclick='reload_problem(5)'>Điểm&nbsp;<span class='glyphicon glyphicon-sort-by-attributes'></span></th>"
                + "</tr>");
    $("#problem-list-table").append(html);

    if (!$("#acm-toggle").is(":checked")) {
        $(".acm").hide();
    }
    if (!$("#oi-toggle").is(":checked")) {
        $(".oi").hide();
    }
}

function cmp_by_column(id) {
    return function (x, y) {
        if (typeof(x[id]) === "string") {
            return (x[id] < y[id]) ? (-1) : (x[id] > y[id]) ? 1 : 0;
        }
        return (x[id] - y[id]) ? (x[id] - y[id]) : (x[0] - y[0]);
    }
}

function reload_problem(id) {
    var cmp_func = cmp_by_column(id);
    problem_list.sort(cmp_func);
    load_problem_list();
}

function reload_user(id) {
    var cmp_func = cmp_by_column(id);
    rank_users.sort(cmp_func);
    load_user_rank();
}
