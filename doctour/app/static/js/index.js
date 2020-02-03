
  $(document).ready(function(){

  env = new nunjucks.Environment(new nunjucks.WebLoader(''),{ autoescape: false });

    $("#search_bar_frame").html(search_bar("major_kw","python Library you try to work with", "Try to work with"))

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

  var loaded = load_loaded()
  if(loaded.success)
  {
        $("#loaded_libs").html(new_panel("Loaded Modules",btn_group(loaded.data)))
  }

    function assign_load_btn(){

        var lib = $(this).data("lib")
        console.log("loading: "+lib)
        load_lib_search_bar(lib)
    }

    $("#major_kw_btn").click(function(){
        var kw = $("#major_kw").val()
        var result = major_search(kw)
        if(result.success)
        {
            var bg = dom("div","btn-group")
            var btns = btn_group([{"id":"load_doc_string","text":"Load Doc String","bstype":"primary"},
            // {"text":"Load Code & Doc String","bstype":"danger"}
          ])
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