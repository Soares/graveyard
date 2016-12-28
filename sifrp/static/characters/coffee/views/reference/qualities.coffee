quality = (sourceDialog) ->
    class Quality extends views.reference.View
        template: '#tmpl-quality-reference'

        events: _.extend
            'change .option': 'update'
            views.reference.View.prototype.events

        context: =>
            abilities = Rulebook.abilities.concat Rulebook.languages
            context =
                brief: @ref.brief
                note: @ref.note
                type: @ref.type
                description: @ref.description
                requirements: @ref.hasRequirements()
            if @ref.choose.ability
                context.abilities = _.pluck abilities, 0
            else context.abilities = false
            if @ref.choose.specialty
                match = ([a, s]) => a is @ref.choose.specialty
                [ability, context.specialties] = _.find abilities, match
            else context.specialties = false
            if @ref.choose.unique
                context.unique = @ref.choose.unique.name
            else context.unique = false
            _.extend @ref.toJSON(), context

        initialize: =>
            if @ref.choose.unique
                @$('.options [name=unique]').autocomplete
                    source: @ref.choose.unique.options

        assign: (@character) =>
            @ref.assign @character
            similar = @ref.similar().length
            if similar
                @header.addClass('posessed').find('.similar').html("(#{similar})")
            else @header.removeClass('posessed').find('.similar').html('')
            do @refresh

        update: (e) =>
            input = $(e.target)
            data = {}
            data[input.attr 'name'] = input.val()
            @ref.set data
            do @refresh

        refresh: =>
            passed = @$('.passed').html('')
            failed = @$('.failed').html('')
            wrapPass = (msg) -> $('#tmpl-quality-passed').tmpl message: msg
            wrapFail = (msg) -> $('#tmpl-quality-failed').tmpl message: msg
            wrap = (str) => @make 'div', class: 'requirement', str
            pass = (msg) => passed.append wrapPass msg.toString()
            fail = (msg) => failed.append wrapFail msg.toString()
            @ref.check pass, fail

        close: => sourceDialog().open (source) =>
            @list.close @results(source)

        results: (source) =>
            ref = @ref.clone()
            ref.set source: source
            return ref

Benefit = quality -> benefitSource
Drawback = quality -> drawbackSource


class Qualities extends views.reference.List
    assign: (character) => _.each @refs, (ref) => ref.assign character
class Benefits extends Qualities
    el: '#benefit-reference'
    view: Benefit
    listing: -> (new q name: name) for name, q of Rulebook.benefits
class Drawbacks extends Qualities
    el: '#drawback-reference'
    view: Drawback
    listing: -> (new q name: name) for name, q of Rulebook.drawbacks


sourceDialog = (el) ->
    class SourceDialog extends views.Dialog
        el: el
        initialize: => @$('.buttonset').buttonset()
        results: => @$('[name=source]:checked').val()
        buttons:
            record: 'close'
DrawbackSourceDialog = sourceDialog '#drawbackSource-dialog'
BenefitSourceDialog = sourceDialog '#benefitSource-dialog'


characters.bind 'focus', (c) ->
    views.reference.benefits or= new Benefits
    views.reference.drawbacks or= new Drawbacks
    views.reference.benefits.assign(c)
    views.reference.drawbacks.assign(c)
drawbackSource = benefitSource = null
$ ->
    benefitSource = new BenefitSourceDialog
    drawbackSource = new DrawbackSourceDialog
