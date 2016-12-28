views.reference = {}

class views.reference.View extends views.View
    events:
        'click button.select': 'close'
    constructor: (@ref, @list) ->
        render = _.map @render(), $
        @header = _.find render, (e) -> e.is '.header'
        @content = _.find render, (e) -> e.is '.content'
        @list.push @header, @content
        super el: @content
        @$('button.select').button()
    render: => $(@template).tmpl @context()
    context: -> _.extend {}, @ref
    results: => @ref
    close: => @list.close @results()


class views.reference.List extends views.Dialog
    options:
        width: '500px'
        height: 'auto'
    constructor: ->
        super
        listing = @listing
        if _.isFunction listing then listing = listing()
        @refs = _.map listing, (ref) => new @view ref, this
        @el.accordion autoHeight: false
    push: (header, content) => @el.append(header).append(content)
    close: (results) =>
        @el.dialog 'close'
        results = [results] unless _.isArray results
        if @callback then @callback results...
