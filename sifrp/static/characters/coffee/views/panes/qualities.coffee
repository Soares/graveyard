class Quality extends views.panes.Model
    template: '#tmpl-quality'
    areYouSure: 'Are you sure you want to remove this benefit?'
    activate: =>
        @$('button.open').button
            text: false
            icons: primary: 'ui-icon-circle-plus'
    context: =>
        c = super
        console.log 'CHECK CONTEXT OPTIONS FOR', @, c
        # FIX THIS THING TO SHOW OPTIONS IN CONTEXT.
        # THEY NEED TO BE CORRECTLY SET BY THE REFERENCE
        return c


class Qualities extends views.panes.List
    view: Quality
    events:
        'click .header .open': 'open'
    activate: =>
        @$('.header .open').button
            text: false
            icons: primary: 'ui-icon-circle-plus'
    push: (benefit) => @$('.content').append benefit
    record: (quality) => @model.add quality
class Benefits extends Qualities
    el: '#benefits'
    getModel: (character) -> character.get 'benefits'
    open: => views.reference.benefits.open(@record)
class Drawbacks extends Qualities
    el: '#drawbacks'
    getModel: (character) -> character.get 'drawbacks'
    open: => views.reference.drawbacks.open(@record)


characters.attach Benefits
characters.attach Drawbacks
