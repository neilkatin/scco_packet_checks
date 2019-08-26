

import logging

import jinja2

log = None

class Output(object):

    def main_template(self):
        """ return the main jinja2 template """

        return """

SCCo ARES/RACES Packet Practice Report.  Accepting messages starting
{{ window_start.strftime(date_format) }} and before {{ window_end.strftime(date_format) }}.

----------------------- DAY'S SUMMARY -----------------------
Totals:
  All messages:            {{ "{0:2d}".format(msgs_all) }} received;  {{ "{0:2d}".format(msgs_correct_cnt) }} ({{ "{0:3.0f}".format(msgs_correct_pct) }}%) correct. [includes duplicates]
  Unique "from" addresses: {{ "{0:2d}".format(results.get_unique_from_count()) }}
  Unique "users":          {{ "{0:2d}".format(results.get_unique_user_count()) }} (report this to the net)

Simulated BBS outage: {{ results.down_bbs }}
  {{ results.down_msg_keys }}/{{ msgs_all }} ({{ "{0:2.1f}".format((results.down_msg_keys * 100.0)/msgs_all) }}%) incorrectly sent FROM this BBS.

Sources:
  Santa Clara County BBSs: {{ results.get_source_xsc_total() }}
    {{ "{0:2d}".format(results.get_source_xsc(1)) }} W1XSC
    {{ "{0:2d}".format(results.get_source_xsc(2)) }} W2XSC
    {{ "{0:2d}".format(results.get_source_xsc(3)) }} W3XSC
    {{ "{0:2d}".format(results.get_source_xsc(4)) }} W4XSC

  Other: {{ results.get_source_other() }}


Most operators who sent a message that is flagged in the list below
will automatically receive a reply with additional details and suggested
corrective actions. If your message is flagged, please retrieve the detailed
reply message from the BBS, email provider, or other service you used to
submit the weekly packet practice message before requesting assistance.

----------------------- DAY'S DETAILS -----------------------

## FROM                                SUBJECT
{% for key in results.get_msg_keys() -%}
{%- set msg = mbox.get(key) %}
{{ "{0:>2d}".format(loop.index0) }} {{ "{0:<35s}".format(msg.get("from", "<no from>"))|e }} {{ msg.get("subject", "<no subject>")|e }}
{%- set errors = results.get_msg_errors(key) -%}
{%- if errors %}
   {% for error in errors %}
     {{ error.error_string }}
   {%- endfor %}
{% endif -%}
{%- endfor %}


Practice Message counts:
    {% for body_type in results.get_body_types()|sort %}
    {% set count = results.get_body_type_count(body_type) -%}
    {{ "{0:2d}".format(count) }} {{ body_type }} messages
    {%- endfor %}

This list created by K2ll, Neil Katin
Script run: {{ now.strftime("%Y-%m-%d %H:%M:%S %Z") }}

        """

    def main_output(self, results, mbox, now, show_output, window_start, window_end):

        global log

        if log is None:
            log = logging.getLogger(__name__)

        template_text = self.main_template()

        template = jinja2.Template(template_text)

        msgs_all = results.total_msg_keys
        msgs_correct_cnt = results.total_msg_keys_correct
        msgs_correct_pct = msgs_correct_cnt * 100 / msgs_all

        params = {
                'run_date': f"{now:%A, %B %d %Y}",
                'msgs_all': msgs_all,
                'msgs_correct_cnt': msgs_correct_cnt,
                'msgs_correct_pct': msgs_correct_pct,
                'mbox': mbox,
                'now': now,
                'results': results,
                'window_start': window_start,
                'window_end': window_end,
                'date_format': '%Y-%m-%d %H:%M:%S'
                }
        output = template.render(params)

        if show_output:
            print("----- main program output -----")
            print(output)
        else:
            log.debug(output)



