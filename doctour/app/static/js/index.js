
  $(document).ready(function(){
  nunjucks.configure( { autoescape: false })

    $("#search_bar_frame").html(search_bar("major_kw","python Library you try to work with", "Try to work with"))

    function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
        }

    function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
        }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
        }
    }
    return "";
    }

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
    function search_bar(name, placeholder,btn_text)
    {
    return nunjucks.render('static/templates/search_bar.html',{name:name,placeholder:placeholder,btn_text:btn_text})
    }
    function search_result(lib,results)
    {
    return nunjucks.render("static/templates/search_result.html",{results:results,lib:lib})
    }

  function load_loaded(){
   var aj=$.ajax({
    url:"/doc/list_all/",
    method:"POST",
    async:false,
    contentType: 'application/json;charset=UTF-8',
    success:function(data){console.log(data);return data}
   })
   return aj.responseJSON
  }
  var loaded = load_loaded()
  console.log(loaded)
  if(loaded.success)
  {
        $("#loaded_libs").html(new_panel("Loaded Modules",btn_group(loaded.data)))
  }

    function get_lib_index(lib)
    {
        var aj = $.ajax({
            url:"/lib/add/",
            data:JSON.stringify({"lib":lib}),
            async: false,
            method:"POST",
            contentType: 'application/json;charset=UTF-8',
            success:function(data){
             if(data.success)
             {
             console.log("start load search index")
                var index = elasticlunr(function () {
                this.addField('name');
                this.addField('path');
                this.setRef('id');
                });
                for(doc in data.data.frame) {index.addDoc(data.data.frame[doc]);}
                window.idx = index
                return index
             }
             else
             {
                return data.data
             }
            }
            })
       return aj.responseJSON
    }

    function assign_load_btn(){

        var lib = $(this).data("lib")
        console.log("loading: "+lib)
        get_lib_index(lib)
        $("#inlib_search_bar").html(search_bar("search_lib","Search In Library: "+lib, false))
        $("#inlib_search_result").html(null)
        $("#search_lib_btn").click(function(){
            var kw = $("#search_lib").val();
            var results = window.idx.search(kw)
            console.log(results)
            if(results.length==0){$("#inlib_search_result").html(new_panel("Nothing found","Nothing found about: "+String(kw)+ " , Please try again"))}
            else{
            $("#inlib_search_result").html(search_result(lib,results))
            }
        })
    }

    $("#major_kw_btn").click(function(){
        var kw = $("#major_kw").val()
        var result = major_search(kw)
        if(result.success)
        {
            var bg = dom("div","btn-group")
            var btns = btn_group([{"id":"load_doc_string","text":"Load Doc String","bstype":"primary"},{"text":"Load Code & Doc String","bstype":"danger"}])
            var p = new_panel("Library Found: "+result.data.name, btns)
            $("#major_search_result").html(p)
            $("#inlib_search_bar").html(null)
            $("#inlib_search_result").html(null)
            $("#load_doc_string").data("lib",kw)
            $("#load_doc_string").click(assign_load_btn)
        }
        else
        {
            $("#major_search_result").html(new_panel("Library Not Found",result.data.error))
        }
    })

  })