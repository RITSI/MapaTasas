from django import template
from cookielaw.templatetags.cookielaw_tags import CookielawBanner

register = template.Library()

class CookielawAlert(CookielawBanner):
    template = 'tasas/banner.html'

register.tag(CookielawAlert)