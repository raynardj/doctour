function new_panel(title, content)
{ return env.render('static/templates/panel.html',{"title":title, "content":content})}

function btn(conf)
    { return env.render('static/templates/btn.html',conf) }

function traceup_render(result)
{   return env.render('static/templates/traceup.html',result)
}

function btn_group(btns)
    {
        return env.render('static/templates/btn_groups.html',{"btns":btns})
    }
function search_bar(name, placeholder,btn_text)
    {
        return env.render('static/templates/search_bar.html',{name:name,placeholder:placeholder,btn_text:btn_text})
    }
function search_result(lib,results)
    {
        return env.render("static/templates/search_result.html",{results:results,lib:lib})
    }
function load_loaded(){
   var aj=$.ajax({
    url:"/doc/list_all/",
    method:"POST",
    async:false,
    contentType: 'application/json;charset=UTF-8',
    success:function(data){return data}
   })
   return aj.responseJSON
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
                this.addField('alias');
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

function load_lib_search_bar(lib)
    {
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