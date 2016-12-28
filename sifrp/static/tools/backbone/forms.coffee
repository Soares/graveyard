# A helper function to get the val of `input`. For radios, this is the .val()
# of the checked input; for checkboxes this is either 'true' or 'false', for
# all other inputs it's jQuery's .val()
getinput = (input) ->
    if input.is '[type=radio]' then input.filter(':checked').val()
    else if input.is '[type=checkbox]' then input.is ':checked'
    else input.val()


# A helper function to set the input to the given value. Radios and checkboxes
# are either checked or unchecked, all other inputs use jQuery's .val()
setinput = (input, value) ->
    if input.is '[type=radio]'
        input.removeAttr 'checked'
        input.filter("[value=#{value}]").attr 'checked', 'checked'
    else if input.is '[type=checkbox]'
        if value then input.attr 'checked', 'checked'
        else input.removeAttr 'checked'
    else input.val value


# A view that links a form to a model. Give it a 'links' object of key-value
# pairs, where the keys are model field names and the values are selectors
# that match input elements. A blank selector will match @el.
# Any updates to model attributes will be pushed to the inputs, and any changes
# to the inputs will be pushed to the model.
class Backbone.FormView extends Backbone.View
    # A helper function to get the input matched by `selector`, which will be
    # @el if `selector` is blank.
    input: (selector) => if selector then @$(selector) else $(@el)

    # This cleans 'value' (which comes from the form) before setting it as
    # 'field' in the model. Instead of overriding this function, you should
    # set field: fn(value) pairs in the 'cleaners' object.
    clean: (field, value) =>
        if @cleaners?[field] then @cleaners[field].apply this, [value]
        else value

    # This cleans 'value' (which comes from the model) for display by the form.
    # Instead of overriding this function, you should set field: fn(value)
    # pairs in the 'displayers' object.
    display: (field, value) =>
        if @displayers?[field] then @displayers[field].apply this, [value]
        else value

    # Bind the input elements on the web page to update the model when changed
    # This method need only be called when @el is created, it need not be
    # called every time @model is changed.
    delegateFormEvents: (links=@links) =>
        changeEvent = "change.delegateLinks#{@cid}"
        $(@el).unbind ".delegateLinks#{@cid}"
        for field, selector of links
            do (field, selector) =>
                changeFn = (e) =>
                    input = $ e.target
                    value = @clean field, getinput input
                    if _.isEqual value, @model.get field
                        input.val @display field, value
                    else
                        data = {}
                        data[field] = value
                        @model.set data
                if selector is '' then $(@el).bind changeEvent, changeFn
                else $(@el).delegate selector, changeEvent, changeFn
        return this

    # Bind the model attribute change events to update the form elements on the
    # page. This method must be called every time @model is changed.
    delegateModelEvents: (links=@links) =>
        for field, selector of links
            do (field, selector) =>
                @model.bind "change:#{field}", (model, val) =>
                    setinput @input(selector), @display(field, val)
        return this

    # Update the web page with the current state of the model. This need only be
    # called the first time that @model is set, to ensure that every model field
    # is set on the inputs. After the first time, fields will update themselves
    # when model 'change' events are fired.
    pushModelToForm: (links=@links) =>
        for field, selector of links
            setinput @input(selector), @display(field, @model.get field)
        return this

    # Reassign @model, re-delegate the appropriate events, and update the html
    # form if necessary.
    reassign: (@model) =>
        do @delegateModelEvents
        do @pushModelToForm

    # Delegates the form events, and the model events if @model is given.
    constructor: ->
        super
        do @delegateFormEvents
        if @model then @reassign @model
