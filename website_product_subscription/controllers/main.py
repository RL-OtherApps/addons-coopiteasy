# -*- coding: utf-8 -*-
import base64
import datetime
import re

import werkzeug
import werkzeug.urls

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _


class WebsiteProductSubscription(http.Controller):
    
    @http.route(['/page/become_subscriber','/become_subscriber'], type='http', auth="public", website=True)
    def display_subscription_page(self, **kwargs):
        values = {}

        values = self.fill_values(values, True)
        
        for field in ['email','firstname','lastname','birthdate','iban','share_product_id','no_registre','address','city','zip_code','country_id','phone','lang','nb_parts','total_parts','error_msg']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        
        values.update(kwargs=kwargs.items())
        return request.website.render("website_product_subscription.becomesubscriber", values)
    
    def fill_values(self, values, load_from_user=False):
        if load_from_user:
            if request.env.user.login != 'public':
                values['logged'] = 'on'
                partner = request.env.user.partner_id
                values['firstname'] = partner.firstname
                values['lastname'] = partner.lastname
                values['email'] = partner.email
                values['street'] = partner.street
                values['zip_code'] = partner.zip
                values['city'] = partner.city
                values['country_id'] = partner.country_id.id
                if partner.parent_id:
                    values['company'] = partner.parent_id.display_name
        
        if not values.get('product_subscription_id',False):
            values['product_subscription_id'] = 0
        values['subscriptions'] = request.env['product.subscription.template'].sudo().search([('publish','=',True)])
        values['countries'] = self.get_countries()
        
        if not values.get('country_id'):
            values['country_id'] = '21'    
        return values 
    
    def get_countries(self):
        countries = request.env['res.country'].sudo().search([])
        
        return countries
    
    def get_address(self, kwargs):
        vals = {'zip':kwargs.get("zip_code"),
                'city':kwargs.get("city"),
                'country_id':kwargs.get("country_id")}
        vals['street'] = kwargs.get("street") +', ' + kwargs.get("street_number") +', ' + kwargs.get("box") 
        return vals
    
    def get_receiver(self, kwargs):
        vals = {'email': kwargs.get("subscriber_email")}
        firstname = kwargs.get("subscriber_firstname").title()
        lastname = kwargs.get("subscriber_lastname").upper()
        vals['name'] =  firstname + ' ' + lastname
        vals['firstname'] = firstname
        vals['lastname'] = lastname
        
        return vals

    @http.route(['/product_subscription/subscribe'], type='http', auth="public", website=True)
    def share_subscription(self, **kwargs):
        partner_obj = request.env['res.partner']
        values = {}
        redirect = "website_product_subscription.becomesubscriber"
        
        if not kwargs.has_key('g-recaptcha-response') or not request.website.is_captcha_valid(kwargs['g-recaptcha-response']):
           values = self.fill_values(values)
           values.update(kwargs)
           values["error_msg"] = "the captcha has not been validated, please fill in the captcha"
           
           return request.website.render(redirect, values)
        
        logged = kwargs.get("logged")=='on'
        if logged and kwargs.get("email") != kwargs.get("email_confirmation"):
            values = self.fill_values(values)
            values.update(kwargs)
            values["error_msg"] = "email and confirmation email doesn't match"
            return request.website.render(redirect, values)
        
        gift = False
        if kwargs.get("gift") == 'on':
            gift = True
            values["gift"] = gift

        subscriber = False
        sponsor = False
        subscriber_vals = {}
        if logged:
           subscriber = request.env.user.partner_id
           address = self.get_address(kwargs)
           if gift:
               sponsor = request.env.user.partner_id
               subscriber_vals.update(self.get_receiver(kwargs))
               subscriber_vals.update(address)
               subscriber = partner_obj.create(subscriber_vals)
           else:
                subscriber.write(address) 
        else:
            lastname = kwargs.get("lastname").upper()
            firstname = kwargs.get("firstname").title()
            
            subvalues["name"] = firstname + " " + lastname
            subscriber_vals["lastname"] = lastname
            subscriber_vals["firstname"] = firstname
            subscriber_vals["email"] = kwargs.get("email").title()
            if gift:
                receiver_vals= self.get_receiver(kwargs)
                receiver_vals.update(self.get_address(kwargs))
                subscriber = partner_obj.create(receiver_vals)
                sponsor = partner_obj.create(subscriber_vals)
            else:
                subscriber_vals.update(self.get_address(kwargs))
            subscriber = partner_obj.create(subscriber_vals)
            values['subscriber'] = subscriber
            values['sponsor'] = sponsor
            
        values["subscription_template"] = int(kwargs.get("product_subscription_id"))
        
        request.env['product.subscription.request'].sudo().create(values)

        return self.get_subscription_response(values, kwargs)