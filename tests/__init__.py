#
# Copyright (c) 2013-2014 QuarksLab.
# This file is part of IRMA project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.


import sys
import os

pardir = os.path.abspath(os.path.join(__file__, os.path.pardir))
sys.path.append(os.path.dirname(pardir))
cwd = os.path.abspath(os.path.dirname(__file__))
os.environ['IRMA_BRAIN_CFG_PATH'] = cwd

from brain.models.sqlobjects import Base, SQLDatabase
Base.metadata.drop_all(SQLDatabase.get_engine())
Base.metadata.create_all(SQLDatabase.get_engine())
