#    Blockchain, and web3 technology aggregator 
#    Copyright © 2024 Charudatta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    email contact: 152109007c@gmailcom

set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

local__path := "C:/Users/$env:username/Documents/GitHub/"

default:
    @just --choose

# create files and directories
init:
    #!pwsh
    $ProjectName = Read-Host "Enter your project name"
    Initialize-Project -ProjectName $ProjectName

# add documentation to repo
docs:
    #!pwsh
    mkdocs build

# version control repo with git
commit message="init":
    #!pwsh
    git add .
    git commit -m {{message}}

# create windows executable
exe file_name:
    #!pwsh
    pyinstaller src/{{file_name}} --onefile
 
# exit just file
quit:
    #!pwsh
    write-Host "Copyright © 2024 Charudatta"
    
# deploy application
deploy:
    #!pwsh
    $CommitMessage = Read-Host "Enter your commit message"
    Invoke-DeployChecks -CommitMessage $CommitMessage

# view logs
view-logs:
    #!pwsh
    Get-Content -Path "app.log" -Tail 10

# clean up
clean:
    #!pwsh
    Remove-Item -Recurse -Force dist, build, *.egg-info

# project mangement add task and todos 
tasks:
    #!pwsh
    python {{local__path}}"project-manager/src/project-manager-cli"

# Add custom tasks, enviroment variables

# run project
# run:
#    #!pwsh
#   python run.py
