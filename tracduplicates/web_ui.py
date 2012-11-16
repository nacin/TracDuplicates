from genshi.builder import tag

from trac.core import *
from trac.ticket.api import ITicketActionController
from trac.ticket.model import Ticket
from trac.ticket.default_workflow import ConfigurableTicketWorkflow


class TicketProxy:
  def __init__(self, dupe_id, ticket):
    self._dupe_id = dupe_id
    self._ticket = ticket
    ticket._proxy_old_save = ticket.save_changes
    ticket.save_changes = self.save_changes

  def save_changes(self, author, comment, when=0, db=None, cnum=''):
    if not comment or not len(comment.strip()):
      comment = "Duplicate of #%d." % self._dupe_id
    elif -1 == comment.find('#' + str(self._dupe_id)):
      comment = "Duplicate of #%d.\n\n%s" % (self._dupe_id, comment)

    dupeticket = Ticket(self._ticket.env, self._dupe_id, db=db)
    dupeticket.save_changes(
      author,
      "#%d was marked as a duplicate." % self._ticket.id,
      when=when,
      db=db
      )

    return self._ticket._proxy_old_save(author, comment, when=when, db=db, cnum=cnum)

class DuplicatesWorkflow(Component):
  implements(ITicketActionController)

  # ITicketActionController
  def get_ticket_actions(self, req, ticket):
    controller = ConfigurableTicketWorkflow(self.env)
    return controller.get_actions_by_operation_for_req(req, ticket, 'set_duplicate')


  def get_all_status(self):
    return []

  def render_ticket_action_control(self, req, ticket, action):
    controll = tag.input(type='text', id='action_dupe', size=5, name='action_dupe', value=req.args.get('action_dupe', '').replace('#', ''))
    return ('dupe to', controll, '(marked duplicate)')

  def get_ticket_changes(self, req, ticket, action):

    if not req.args.get('action_dupe'):
      return {}

    db = self.env.get_db_cnx()
    comment = req.args.get('comment')
    try:
      dupeid = int(req.args.get('action_dupe').replace('#', ''))
      Ticket(self.env, dupeid, db=db)
      TicketProxy(dupeid, ticket)
    except (ValueError, TypeError, TracError):
      raise Exception("Invalid ticket ID specified. Can't mark as duplicate.")

    return {
        'status': 'closed',
        'resolution': 'duplicate'
        }

  def apply_action_side_effects(self, req, ticket, action):
    pass
