
  $(document).ready(function(){
  env = new nunjucks.Environment(new nunjucks.WebLoader('../../../..',),{ autoescape: false });
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
     item.data.code = get_code(query.lib,item.data.names[0])
     return env.render("../../../../static/templates/read_doc.html",item.data)
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

  $("#content_detail").html(read_doc())

  })