import base64
from odoo import http 
from odoo.http import request

class RealEstate(http.Controller):
    
    # Property form page
    @http.route('/property_form', type='http', auth='user', website=True)
    def property_form(self, **kw):
        #property tag value search
        PropertyTag = http.request.env['property.tags']
        property_tags = PropertyTag.search([])
        
        #property types value search
        PropertyType = http.request.env['property.type']
        property_types = PropertyType.search([])
        
        #state value search
        State = http.request.env['res.country.state']
        states = State.search([])
        
        #country value search
        Country = http.request.env['res.country']
        countries = Country.search([])
        
        # property_image = None
        # if 'property_image' in request.httprequest.files:
        #     property_images = request.httprequest.files.get('property_image')
        #     # property_images = property_images.read()
        #     property_image = property_images.encode('base64')
        #     property_image = base64.b64encode(property_image)
        
        garden_orientations = request.env['real.estate'].fields_get(allfields=['garden_orientation'])['garden_orientation']['selection']
        
        return http.request.render('estate.create_property',{'property_types': property_types,
                                                            'property_tags': property_tags,
                                                            'garden_orientations': garden_orientations,
                                                            'states':states,
                                                            'countries':countries,
                                                            # 'property_image': property_image,
                                                            })
    
    # Redirect to thank you page
    @http.route('/create/property', type='http', auth='user', website=True)
    def create_property(self,**kw):
        request.env['real.estate'].sudo().create(kw)
        return request.render('estate.user_thanks',{})
    
    # property 
    @http.route(['/properties'], type='http', auth="public", website=True)
    def property_page(self, **kw):
        properties = http.request.env['real.estate'].sudo().search([])
        return http.request.render('estate.property_page', {'properties': properties})
    
    # Show dynamic property details
    @http.route('/properties/<int:property_id>', type='http', auth='public', website=True)
    def property_details(self, property_id, **kw):
        Property = http.request.env['real.estate']
        property = Property.sudo().browse(property_id)
        return http.request.render('estate.property_details',{'property': property})
        
        
    #property page value
    @http.route('/properties/<int:property_id>/create_offer', type='http', auth="user", website=True)
    def create_offer(self, property_id, **post):
        property = request.env['real.estate'].browse(property_id)
        
         #search partner name
        PropertyOffers = http.request.env['property.offer']
        property_offers = PropertyOffers.search([])
        
        
        return request.render('estate.create_offer', {
            'property': property,
            'property_offers' :property_offers,
        })
    
    # Redirect to thank you page
    @http.route('/create/offer', type='http', auth='user', website=True)
    def create_new_offer(self,**kw):
        # request.env['real.estate'].sudo().create(kw)
        
        request.env['property.offer'].sudo().create(kw)
        return request.render('estate.user_thanks',{})
    
    
    # for show user created property
    @http.route('/my_properties', type='http', auth="user", website=True)
    def my_properties(self, **kw):
        return http.request.render('estate.user_created_properties', {})
    
     # Show dynamic user created property details
    @http.route('/my_properties/<int:property_id>', type='http', auth='public', website=True)
    def my_property_details(self, property_id, **kw):
        Property = http.request.env['real.estate']
        property = Property.sudo().browse(property_id)
        return http.request.render('estate.my_property_details',{'property': property})