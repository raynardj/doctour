
  $(document).ready(function(){
  env = new nunjucks.Environment(new nunjucks.WebLoader('../../../..',),{ autoescape: false });
  var loaded = load_loaded()

  function get_id()
  {
    var href= window.location.href
    if(href.charAt(href.length-1)!="/")
    {
        href = href+"/"
    }
    var hlist = href.split("/")
    var id = hlist[hlist.length-2]
    return {id:parseInt(id),lib:String(hlist[hlist.length-3])}
  }
  function get_item(query)
  {
    return $.ajax({
    url:"/doc/read/",
    method:"POST",
    async: false,
    data:JSON.stringify(query),
    contentType: 'application/json;charset=UTF-8',
    }).responseJSON
  }
  function read_doc()
  {
     var query = get_id()
     var item = get_item(query)
     console.log(item)

     if(item.data.code.length < 2)
     {
       var code = get_code(query.lib,item.data.names[0])
        item.data.code = code
     }
     traceup_json = trace_up(query)
     traceup_json.lib = query.lib
     return {detail:env.render("../../../../static/templates/read_doc.html",item.data),traceup:traceup_render(traceup_json), query:query}
  }

  function trace_up(query)
  {
    var lib = query.lib;
    var doc_id = query.id
    return $.ajax({
        url:"/doc/traceup/"+lib+"/"+String(doc_id)+"/",
        method:"POST",
        async:false,
        contentType: 'application/json;charset=UTF-8',
    }).responseJSON
  }

  function get_code(lib,name_chain){
    console.log(name_chain)
    var data = $.ajax({
    url:"/doc/code/",
    method:"POST",
    async: false,
    data:JSON.stringify({lib:lib,name_chain,name_chain}),
    contentType: 'application/json;charset=UTF-8',
    }).responseJSON
    console.log(data)
    if(data.success)
    {
        return data.data.code
    }
  }
    var doc_page = read_doc()
  $("#content_detail").html(doc_page.detail)
   if(loaded.success)
  {
        $("#loaded_libs").html(new_panel("Other Loaded Modules",btn_group(loaded.data)))

  }

    $("#traceup").html(doc_page.traceup)

  })