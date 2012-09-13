import logging, traceback, sys

from django.core.mail import mail_admins
from django.http import QueryDict, HttpResponseServerError, Http404
from django.views.debug import ExceptionReporter

from django.contrib.sites.models import Site

logger = logging.getLogger(__name__)


class ExceptionMiddleware(object):
  """
  Logs the Traceback.
  Mails the admins.
  Shows the Django Error page even when not in DEBUG.

  Great for internal apps behind firewalls with trusted users.
  Something like this is nice for apps with a lot of ajax too.
  """

  def process_exception(self, request, exception):
      current_site = Site.objects.get_current()

      # log the traceback
      tb = traceback.format_exc()
      logger.error('Traceback from %s\n%s' % (request.get_full_path(), tb))

      # if it's a 404 don't email or return special 500 page
      type, val, trace = sys.exc_info()
      if type == Http404:
          return

      # an error besides Http404 and we mail the admins
      subject = 'TRACEBACK from %s: %s' % (current_site, request.get_full_path())
      message = tb
      mail_admins(subject, message, fail_silently=True)

      # return the DEBUG 500 page to the client
      er = ExceptionReporter(request, *sys.exc_info())
      return HttpResponseServerError(er.get_traceback_html())
