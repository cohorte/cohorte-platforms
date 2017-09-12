cohorte-start-node
==================

    When choosing a transport mode, we have the following possibilities depending on the deployment schema.


    Application running on "one node"
    ---------------------------------
        The isolates of one node are discovered using an internal discovery protocol and communicates between them using http servlets.

        possible transport configurations :  [ ]            
        ----------------------------------------------------
        used transport protocol           :  http servlet   
        used discovery protocol           :  local discovery


    Application running on "several nodes in the same LAN"
    ------------------------------------------------------

        In addition to the local discovery of isolates of the same node, users should set the "transport" configuration to "http" in "run.js" file or via "--transport http" argument of "run" command. This "http" transport adds the "multicast" discovery protocol to retrive isolates of the same application located on different nodes of the same LAN network. 

        possible transport configurations :  ["http"]    
        -------------------------------------------------
        used transport protocol           :  http servlet
        used discovery protocol           :  multicast   


    Application running on "several nodes in a WAN"
    -----------------------------------------------

        When the nodes of the same application are deployed on nodes over Internet, users should choose "xmpp" transport when starting the nodes.

        possible transport configurations :  ["xmpp"]    
        -----------------------------------------------------
        used transport protocol           :  xmpp chat server
        used discovery protocol           :  xmpp rooms   

