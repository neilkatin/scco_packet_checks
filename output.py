

import logging

import jinja2

log = None

class Output(object):

    def main_template(self):
        """ return the main jinja2 template """

        return """

SCCo ARES/RACES Packet Practice Report For: {{ run_date }}

----------------------- DAY'S SUMMARY -----------------------
Totals:
  All messages:            {{ msgs_all        }} received;  {{ msgs_correct_cnt        }} ({{ msgs_correct_pct }}%) correct. [includes duplicates]
  Unique "from" addresses: {{ unique_all      }} received;  {{ unique_correct_cnt      }} ({{ unique_correct_pct }}%) correct. [unique From: addresses]
  Unique call signs:       {{ unique_call_all }} received;  {{ unique_call_correct_cnt }} ({{ unique_call_correct_pct }}%) correct. [{{ unique_correct_cnt }} reported to main net]

Simulated BBS outage: {{ results.down_bbs }}
  0/21 (0%) incorrectly sent FROM this BBS.

Sources:
      Santa Clara County BBSs: 20
      13 W1XSC
       2 W2XSC
       0 W3XSC
       5 W4XSC

  Other: 1
      1 from E-Mail.


Most operators who sent a message that is flagged in the list below
will automatically receive a reply with additional details and suggested
corrective actions. If your message is flagged, please retrieve the detailed
reply message from the BBS, email provider, or other service you used to
submit the weekly packet practice message before requesting assistance.

----------------------- DAY'S DETAILS -----------------------

## FROM                                SUBJECT
{% for key in results.get_valid_msg_keys() -%}
{%- set msg = mbox.get(key) %}
{{ "{0:>2d}".format(loop.index0) }} {{ "{0:<35s}".format(msg.get("from", "<no from>"))|e }} {{ msg.get("subject", "<no subject>")|e }}
{%- endfor %}

Practice Message count:
    0 other messages
   NN SCCoPIFO messages

This list created by K2ll, Neil Katin
Script run: {{ now.isoformat() }}

        """

    def main_output(self, results, mbox, now):

        global log

        if log is None:
            log = logging.getLogger(__name__)

        template_text = self.main_template()

        template = jinja2.Template(template_text)

        params = {
                'run_date': f"{now:%A, %B %d %Y}",
                'msgs_all': "<TODO>",
                'msgs_correct_cnt': "<TODO>",
                'msgs_correct_pct': "<TODO>",
                'unique_all': "<TODO>",
                'unique_correct_cnt': "<TODO>",
                'unique_correct_pct': "<TODO>",
                'unique_call_all': "<TODO>",
                'unique_call_correct_cnt': "<TODO>",
                'unique_call_correct_pct': "<TODO>",
                'mbox': mbox,
                'now': now,
                'results': results
                }
        output = template.render(params)

        log.debug(output)



