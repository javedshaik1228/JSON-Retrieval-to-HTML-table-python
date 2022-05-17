    <script src="http://code.jquery.com/jquery-1.8.3.js"></script>
    <script src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css" />

    <style>
        .ui-menu { width: 220px; z-index: 100; }
        #menu { width: 220px; z-index: 100; }
    </style>
    <ul id="menu">
        <li>
            <a href="#">Menu</a>
            <ul>
                <li><a href="evoucher_display.php">Display EVR blob</a></li>
                <li><a href="changeLog.php">Change Log</a></li>
                <li>
                    <a href="#">Config distrib</a>
                    <ul>
                        <li><a href="master_chain_config.php">Master Chains</a></li>
                        <li><a href="retrieve_chain_config.php">Chain level</a></li>
                        <li><a href="retrieve_hotel_config.php">Property level</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">Dashboards</a>
                    <ul>
                        <li><a href="componentStatus.php?comp=rsd">RSD</a></li>
                        <li><a href="componentStatus.php?comp=sbi">SBI</a></li>
                        <li><a href="componentStatus.php?comp=hrs">HRS</a></li>
                        <li><a href="componentStatus.php?comp=sba">SBA</a></li>
                        <li><a href="componentStatus.php?comp=cui">CUI</a></li>
                        <li><a href="resaVersions.php">Resa Versions</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">LQS</a>
                    <ul>
                        <li><a href="pollLQS.php">Poll LQS</a></li>
                        <li><a href="retrieveLQSItem.php">retrieve item</a></li>
                    </ul>
                </li>
                <li>
                    <a href="retrieve_hoteltdc.php">Hotel Descriptive Content</a>
                </li>
                </li>
                <li>
                    <a href="#">Rates</a>
                    <ul>
                        <li><a href="retrieve_agg.php">Investigate agg</a></li>
                        <li><a href="import_property.php">Import property</a></li>
                        <hr/>
                        <li><a href="retrieve_agg.php?table=agg_viewership">Agg viewership</a></li>
                        <li><a href="retrieve_agg.php?table=agg_sequencing">Agg sequencing</a></li>
                        <li><a href="retrieve_agg.php?table=agg_rateplan">Agg rateplan</a></li>
                        <li><a href="retrieve_agg.php?table=agg_property">Agg property</a></li>
                        <li><a href="retrieve_agg.php?table=agg_chain">Agg chain</a></li>
                        <hr/>
                        <li><a href="retrieve_tax.php">Hrp Tax</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">Links</a>
                    <ul>
                        <li>
                            <a href="#">Deco</a>
                            <ul>
                                <li><a href="http://ncegcolnx310.nce.amadeus.net:20099/cgi-bin/LoggedContextRetriever/retrieve.pl">Logged PNR Context Retriever</a></li>
                                <li><a href="http://ncegcolnx310.nce.amadeus.net:20099/cgi-bin/LiveContextRetriever/retrieve.pl">Live PNR Context Retriever</a></li>
                                <li><a href="http://ncegcolnx310.nce.amadeus.net:20099/cgi-bin/TpfRecordExtrator/extract.pl">TPF record extractor</a></li>
                                <li><a href="http://ncegcolnx238:30005/link_graph/">Links Generator</a></li>
                                <li><a href="http://ncegcolnx310.nce.amadeus.net:20099/cgi-bin/EztReader/ezt_reader.pl">ROC EZTable Reader</a></li>
                                <li><a href="http://ncegcolnx310.nce.amadeus.net:20099/cgi-bin/ConversionLibRetriever/LibsOfObe2Tpf.pl">Conversion Libraries in Obe2Tpf and Tpf2Obe Packs</a></li>
                                <li><a href="http://ncegcolnx310.nce.amadeus.net:20099/DcxEventLog/">DCX EventLog</a></li>
                                <li><a href="http://ncegcolnx310.nce.amadeus.net:20099/RI/">RI Services</a></li>
                                <li><a href="http://platinum/scs/CONVERSION/">ConvLibs Pt</a></li>
                                <li><a href="http://jenkins/scs/view/CONVERSION/">ConvLibs jenkins</a></li>
                                <li><a href="https://internalcommunities.amadeus.com/sites/pnr-portal/ARS-RLF/default.aspx">RLF Home Page</a></li>
                                <li><a href="https://internalcommunities.amadeus.com/sites/pnr-portal/rfc/default.aspx">RFC Home page</a></li>
                                <li><a href="https://internalcommunities.amadeus.com/sites/devsup/api/Lists/OSRs%20planning%20PRD/calendar.aspx?CalendarDate=13%2F02%2F2012">SI OSR Planning</a></li>
                                <li><a href="http://gcnet-tst/~cdeguet/TPFDeco/dashboard.html">Deco Dashboard</a></li>
                            </ul>
                        </li>
                        <li>
                            <a href="#">SI config </a>
                            <ul>
                                <li><a href="http://mucosr01.os.amadeus.net:8080/application/oneosr/siosr/dashboard/">SI OSR</a></li>
                                <li><a href="http://si-wiki/SI/tikiwiki/tiki-index.php?page=LogicalDefinition_RSAP">definition RSAP</a></li>
                                <li><a href="http://si-wiki/SI/tikiwiki/tiki-index.php?page=LogicalDefinition_Route ">definition Route</a></li>
                                <li><a href="http://si-wiki/SI/tikiwiki/tiki-index.php?page=TechnicalDestination">definition Connector</a></li>
                                <li><a href="http://si-wiki/SI/webAdmin/v3/transport_options.php">Transport Options</a></li>
                                <li><a href="http://si-wiki/SI/webAdmin/v3/session_options.php">Session Options</a></li>
                                <li><a href="http://si-wiki/SI/tikiwiki/tiki-index.php">SI wiki</a></li>
                                <li><a href="http://si-wiki/SI/webAdmin/v3/index.php">SI viewer</a></li>
                                <li><a href="http://si-wiki/SI/tikiwiki/tiki-index.php?page=CONTRL+messages">CONTRL messages</a></li>
                                <li><a href="http://hdpdoc/doku.php?id=back-end:delivery:si&s[]=si&s[]=osr">HOS SI OSR procedure</a></li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ul>
        </li>
    </ul>
    <script>
        $( "#menu" ).menu();
    </script>
