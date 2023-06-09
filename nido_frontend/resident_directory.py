#  Nido resident_directory.py
#  Copyright (C) John Arnold
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import (
    Blueprint,
    abort,
    current_app,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import select

from nido_backend.db_models import DBCommunity

from .authentication import login_required
from .main_menu import get_main_menu

bp = Blueprint("resident_dir", __name__)


@bp.route("/")
@login_required
def index():
    gql_query = """
query ResidentDir {
  activeCommunity {
    name
    residences {
      locality
      postcode
      region
      street
      unitNo
      occupants {
        fullName
        groups {
          name
        }
        emails: contactMethods {
          ... on EmailContact {
            email
          }
        }
      }
    }
  }
}"""
    gql_result = g.gql_client.execute_query(gql_query)
    community = gql_result.data.active_community
    main_menu_links = get_main_menu()
    return render_template(
        "resident-dir.html",
        main_menu_links=main_menu_links,
        community=community,
        show_street=True,
    )
