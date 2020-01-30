
  $(document).ready(function(){
  nunjucks.configure( { autoescape: false })
  function major_search(kw){
     var dt = {"kw":kw}
     var aj = $.ajax({
     url:"/search/index/",
     method:"POST",
     data:JSON.stringify(dt),
     async:false,
     contentType: 'application/json;charset=UTF-8',
     success: function(data){
        return data
        }
     })
     return aj.responseJSON
  }
  function dom(objtype,className){
  var obj = document.createElement(objtype);
  obj.className = className
  return obj
  }

    function new_panel(title, content)
    { return nunjucks.render('static/templates/panel.html',{"title":title, "content":content})}

    function btn(conf)
    { return nunjucks.render('static/templates/btn.html',conf) }

    function btn_group(btns)
    {
    return nunjucks.render('static/templates/btn_groups.html',{"btns":btns})
    }

  function json_to_table(j)
  {
    var table = dom("table","table table-hover")
    var thr = dom("tr","")
    var th1 = dom("th","")
    $(th1).html("field")
    var th2 = dom("th","")
    $(th2).html("info")
    table.append(thr)
    thr.append(th1)
    thr.append(th2)
    for(k in j)
    {
        var tr = dom("tr","")
        var td1 = dom("td","")
        var td2 = dom("td","")
        $(td1).append(k)
        $(td2).append(j[k])
        tr.append(td1)
        tr.append(td2)
        table.append(tr)
    }
    return table
  }

    $("#major_kw_btn").click(function(){
        var kw = $("#major_kw").val()
        var result = major_search(kw)
        if(result.success)
        {
            var bg = dom("div","btn-group")
            var btns = btn_group([{"text":"Load Doc String","bstype":"primary"},{"text":"Load Code","bstype":"danger"}])
            var p = new_panel("Library Found: "+result.data.name, btns)
            $("#major_search_result").html(p)
        }
        else
        {
            $("#major_search_result").html(new_panel("Library Not Found",result.data.error))
        }
    })

  })