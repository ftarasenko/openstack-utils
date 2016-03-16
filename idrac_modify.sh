#!/bin/bash

drac_root="root"
drac_pass="calvin"
#servers="127.0.0.1"

pxe1=false
bootorder=false
power=false
inventory=false
qq=false
bootverify=false

while [[ $# -gt 0 ]] && [[ ."$1" = .--* ]] ;
do
  opt=$1;
  shift;
  case "$opt" in
      "--pxe1" ) pxe1=true; echo "Allowing PXE on tthe first NIC";;
      "--bootorder" ) bootorder=true; echo "Changing boot order to use first NIC";;
      "--inventory" ) inventory=true; echo "Collecting inventory data using ipmitool";;
      "--power" ) power=true; echo "And rebooting server";;
      "--queue" ) qq=true; echo "Print queue status";;
      "--bootverify" ) bootverify=true; echo "Verify boot order";;
  esac

done

for server in $servers
do
  if $inventory; then
      nic1_id=`sshpass -p "$drac_pass" ssh "$drac_root"@"$server" "racadm getsysinfo" | grep "NIC.Integrated.1-1-1" | awk '{print \$4}'`
      echo "$server $nic1_id"
  fi
  if $bootverify; then
      bootv=`sshpass -p "$drac_pass" ssh "$drac_root"@"$server" "racadm get BIOS.BiosBootSettings.BootSeq."`
      echo "$server $bootv"
  fi
  if $pxe1; then
      sshpass -p "$drac_pass" ssh "$drac_root"@"$server" "racadm set nic.nicconfig.1.legacybootproto PXE"
      sshpass -p "$drac_pass" ssh "$drac_root"@"$server" "racadm jobqueue create NIC.Integrated.1-1-1"
  fi
  if $bootorder; then
      sshpass -p "$drac_pass" ssh "$drac_root"@"$server" "racadm set BIOS.BiosBootSettings.BootSeq NIC.Integrated.1-1-1"
      sshpass -p "$drac_pass" ssh "$drac_root"@"$server" "racadm jobqueue create BIOS.Setup.1-1"
  fi
  if $qq; then
      status=`sshpass -p "$drac_pass" ssh "$drac_root"@"$server" "racadm jobqueue view" | grep "Message"`
      echo "$server job status is $status"
  fi
  if $power; then
      sshpass -p "$drac_pass" ssh "$drac_root"@"$server" "racadm serveraction powercycle"
      echo "Server $server power cycled"
  fi
done