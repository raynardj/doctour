
  $(document).ready(function(){
  nunjucks.configure( { autoescape: false })

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
     var item = get_item(get_id())
     console.log(item)
     return nunjucks.render("../../../../static/templates/read_doc.html",item.data)
  }

  $("#content_detail").html(read_doc())

  })